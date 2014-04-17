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

import base64
import urllib
import urllib2
import urlparse

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
    "seek": ["seek", "val"],
    "next": ["pl_next"],
    "previous": ["pl_previous"],
    "empty": ["pl_empty"],
    "random": ["pl_random"],
    "loop": ["pl_loop"]
}

URLS = [
    ("youtube.com", "list", "https://gdata.youtube.com/feeds/api/playlists/")
]

DEFAULT_URI = config.get_uri()
VLC_AUTH = b'Basic %s' % base64.b64encode(b':%s' % config.get_vlc_password())

def _encode(action, option):
    """"""
    command = ACTIONS[action]
    tmp = {"command": command[0]}
    if option and len(command) > 1:
        tmp[command[1]] = option
    return urllib.urlencode(tmp)

def _request(file, data=None):
    """VLC does not accept POST requests"""
    if data:
        url = "%s%s?%s" % (VLC_SERVER, file, data)
    else:
        url = "%s%s" % (VLC_SERVER, file)
    #print url
    request = urllib2.Request(url)
    request.add_header('Authorization', VLC_AUTH)
    response = urllib2.urlopen(request)
    return response.read()

def _process_url(action, url):
    """"""
    tmp = urlparse.parse_qsl(url)
    if len(tmp) > 1:
        res = None
        if URLS[0][0] in tmp[0][0] and URLS[0][1] == tmp[1][0]:
            url2 = "%s%s?v=2&max-results=25&start-index=1" % (URLS[0][2], tmp[1][1])
            while url2:
                xml = urllib2.urlopen(urllib2.Request(url2)).readlines()
                url2 = None
                if "<link rel='next'" in xml[0]:
                    url2 = xml[0].split("rel='next'")[1].split("href='")[1].split("'/>")[0]
                    url2 = url2.replace("amp;", "")
                for line in xml:
                    if "src='" in line:
                        v = line.split("src='")[1].split("'")[0]
                        if tmp[0][1] in v:
                            res = _request(STATUS_JSON, _encode(action, v))
                        else:
                            res = _request(STATUS_JSON, _encode("add_enqueue", v))
        return res

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
        if option and option.startswith(("http://", "https://")):
            config.add_url_history(option)
            response = _process_url(action, option)
            if response:
                return response
        return _request(STATUS_JSON, _encode(action, option))
    else:
        return _request(STATUS_JSON)

if __name__ == "__main__":
    #print request_status("toggle_pause", "3071")
    #print request_status("play", "3071")
    print request_status("add_play", DEFAULT_URI)
