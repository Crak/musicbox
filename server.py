#! /usr/bin/env python
###############################################################################
## Musicbox
##
## Copyright (C) 2013-2014 Fran Lupion crakotaku@yahoo.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import sys
import json

import config

import bottle

from vlc_proxy import request_browse, request_status, request_playlist
from musicbox import SoundControl, ProcessManager

BRAND = 'Musicbox'

DEFAULT = {'url': '/'}
SYSTEM = {'url': '/system', 'name': 'System', 'tpl': 'system', 'js': 'system.js'}
PLAYER = {'url': '/player', 'name': 'Player', 'tpl': 'player', 'js': 'player.js'}

def template_values(page):
    values = {'brand': BRAND, 'brand_url': DEFAULT['url']}
    values['title'] = "%s - %s" % (BRAND, page['name'])
    values['script'] =  page['js']
    values['mute'] =  sound.get_mute()
    values['volume'] =  sound.get_volume()
    navs = []
    for p in [PLAYER, SYSTEM]:
        if page == p:
            navs.append({'url': p['url'], 'name': p['name'], 'active': True})
        else:
            navs.append({'url': p['url'], 'name': p['name'], 'active': False})
    values['navs'] = navs
    if page == SYSTEM:
        values['uname'] = manager.get_uname()
        values['uptime'] = manager.get_uptime()
        values['logs'] = manager.get_vlc_log(), manager.get_vnc_log()
    return values
 
@bottle.get('/js/<filepath:path>')    
def serve_javascript(filepath):
    return bottle.static_file(filepath, root='./js/')

@bottle.get('/css/<filepath:path>')
def serve_css(filepath):
    return bottle.static_file(filepath, root='./css/')

@bottle.get('/bootstrap/<filepath:path>')
def serve_bootstrap(filepath):
    return bottle.static_file(filepath, root='./bootstrap/')

@bottle.get('/media/<filepath:path>')
def serve_media(filepath):
    return bottle.static_file(filepath, root='./media/')

@bottle.get(DEFAULT['url'])
@bottle.get(PLAYER['url'])
@bottle.view(PLAYER['tpl'])
def local_player():
    return template_values(PLAYER)
    
@bottle.get(SYSTEM['url'])
@bottle.view(SYSTEM['tpl'])
def system_logs():
    return template_values(SYSTEM)

@bottle.post(DEFAULT['url'])
def sound_manager():
    bottle.response.headers['Content-type'] = 'application/json'
    req = bottle.request.forms.request
    if req == 'sound':
        act = bottle.request.forms.action
        if act == 'mute':
            sound.toggle_mute()
        elif act == 'volume_down':
            sound.volume_down()
        elif act == 'volume_up':
            sound.volume_up()
        return json.dumps({'mute': sound.get_mute(), 'volume': sound.get_volume()})
    elif req == 'standby':
        manager.suspend()
        return json.dumps({})

@bottle.post(PLAYER['url'])
def local_proxy():
    bottle.response.headers['Content-type'] = 'application/json'
    req = bottle.request.forms.request
    if req == 'playlist':
        return request_playlist()
    elif req == 'browse':
        uri = bottle.request.forms.uri
        data = json.loads(request_browse(uri))
        act = bottle.request.forms.action
        if act == 'load':
            data['urls'] = config.get_url_history()
        return json.dumps(data)
    elif req == 'status':
        act = bottle.request.forms.action
        opt = bottle.request.forms.option
        return request_status(act, opt)

@bottle.post(SYSTEM['url'])
def system_manager():
    bottle.response.headers['Content-type'] = 'application/json'
    req = bottle.request.forms.request
    if req == 'logs':
        act = bottle.request.forms.action
        full_logs = False
        if act == 'full':
            full_logs = True
        return json.dumps({
        'vlc_log': manager.get_vlc_log(full_logs), 
        'vnc_log': manager.get_vnc_log(full_logs)
        })
    elif req == 'vlc':
        act = bottle.request.forms.action
        if act == 'restart':
            manager.restart_vlc()
        return json.dumps({'vlc_log': manager.get_vlc_log()})
    elif req == 'vnc':
        act = bottle.request.forms.action
        if act == 'restart':
            manager.restart_vnc()
        return json.dumps({'vnc_log': manager.get_vnc_log()})
    elif req == 'system':
        act = bottle.request.forms.action
        if act == 'quit':
            sys.stderr.close()

if __name__ == '__main__':
    sound = SoundControl()
    manager = ProcessManager()
    bottle.run(host=config.get_host(), port=8081)
