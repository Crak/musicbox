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

import urllib
import urllib2
import base64

import config

VLC_SERVER = "http://localhost:8080/requests/"

PLAYLIST_JSON = "playlist.json"
BROWSE_JSON = "browse.json"
STATUS_JSON = "status.json"

ACTIONS = {
    "add_play": ["in_play", "input"],
    "add_enqueue": ["in_enqueue", "input"],
    "play": ["pl_play", "id"],
    "toggle_pause": ["pl_pause"],
    "stop": ["pl_stop"],
    "next": ["pl_next"],
    "previous": ["pl_previous"],
    "empty": ["pl_empty"],
    "random": ["pl_random"],
    "loop": ["pl_loop"]
}

DEFAULT_URI = config.get_uri()

def _request(file, data=None):
    """VLC does not accept POST requests"""
    if data:
        url = "%s%s?%s" % (VLC_SERVER, file, data)
    else:
        url = "%s%s" % (VLC_SERVER, file)
    #print url
    request = urllib2.Request(url)
    request.add_header('Authorization', b'Basic %s' % base64.b64encode(b':0000'))
    response = urllib2.urlopen(request)
    return response.read()

def request_playlist():
    """"""
    return _request(PLAYLIST_JSON)

def request_browse(uri=None):
    """"""
    if not uri:
        uri = DEFAULT_URI
    return _request(BROWSE_JSON, urllib.urlencode({"uri": uri}))
    
def request_status(action=None, option=None):
    """"""
    if action in ACTIONS:
        command = ACTIONS[action]
        tmp = {"command": command[0]}
        if option and len(command) > 1:
            tmp[command[1]] = option
        return _request(STATUS_JSON, urllib.urlencode(tmp))
    else:
        return _request(STATUS_JSON)

if __name__ == "__main__":
    #print request_status("toggle_pause", "3071")
    #print request_status("play", "3071")
    print request_status("add_play", DEFAULT_URI)
