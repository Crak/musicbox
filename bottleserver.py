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

import json

import config

from bottle import route, view, request, response, static_file, run
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
        values['log'] = manager.get_vlc_log()
    return values
    
@route('/js/<filepath:path>')
def serve_javascript(filepath):
    return static_file(filepath, root='./js/')

@route('/css/<filepath:path>')
def serve_css(filepath):
    return static_file(filepath, root='./css/')

@route('/bootstrap/<filepath:path>')
def serve_bootstrap(filepath):
    return static_file(filepath, root='./bootstrap/')

@route('/media/<filepath:path>')
def serve_media(filepath):
    return static_file(filepath, root='./media/')

@route(DEFAULT['url'])
@route(PLAYER['url'])
@view(PLAYER['tpl'])
def local_player():
    return template_values(PLAYER)
    
@route(SYSTEM['url'])
@view(SYSTEM['tpl'])
def system_logs():
    return template_values(SYSTEM)

@route(DEFAULT['url'], method='POST')
def sound_manager():
    response.headers['Content-type'] = 'application/json'
    req = request.forms.get('request')
    #print "REQUEST: %s" % req
    if req == 'sound':
        act = request.forms.get('action')
        #print "ACTION: %s" % act
        if act == 'mute':
            sound.toggle_mute()
        elif act == 'volume_down':
            sound.volume_down()
        elif act == 'volume_up':
            sound.volume_up()
        return json.dumps({'mute': sound.get_mute(), 'volume': sound.get_volume()})
    elif req == 'standby':
        return json.dumps({})

@route(PLAYER['url'], method='POST')
def local_proxy():
    response.headers['Content-type'] = 'application/json'
    req = request.forms.get('request')
    #print "REQUEST: %s" % req
    if req == 'playlist':
        return request_playlist()
    elif req == 'browse':
        uri = request.forms.get('uri')
        #print "URI: %s" % uri
        return request_browse(uri)
    elif req == 'status':
        act = request.forms.get('action')
        opt = request.forms.get('option')
        #print "ACTION: %s - %s" % (act, opt)
        return request_status(act, opt)

@route(SYSTEM['url'], method='POST')
def system_manager():
    response.headers['Content-type'] = 'application/json'
    req = request.forms.get('request')
    #print "REQUEST: %s" % req
    if req == 'vlc':
        act = request.forms.get('action')
        #print "ACTION: %s" % act
        if act == 'restart':
            manager.restart_vlc()
        elif act == 'reload':
            pass
        return json.dumps({'vlc_log': manager.get_vlc_log()})

if __name__ == '__main__':
    sound = SoundControl()
    manager = ProcessManager()
    run(host=config.get_host(), port=80, debug=True)
