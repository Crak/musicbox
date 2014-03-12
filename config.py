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
import ConfigParser

DEFAULT_SECTION = "DEFAULT"

HOST_OPTION = "bottle_host"
ELEMENT_OPTION = "alsa_element"
USER_OPTION = "system_user"
VLC_PASSWORD_OPTION = "vlc_password"
URI_OPTION = "default_uri"
URL_HISTORY_OPTION = "url_history"

DEFAULTS = {
    HOST_OPTION: "127.0.0.1",
    ELEMENT_OPTION: "PCM",
    USER_OPTION: "musicbox",
    VLC_PASSWORD_OPTION: "0000",
    URI_OPTION: "file:///home/musicbox",
    URL_HISTORY_OPTION: "[]"
}

CONFIG_FILE = "default.cfg"

def get_host():
    """"""
    return config.get(DEFAULT_SECTION, HOST_OPTION)
    
def get_element():
    """"""
    return config.get(DEFAULT_SECTION, ELEMENT_OPTION)

def get_user():
    """"""
    return config.get(DEFAULT_SECTION, USER_OPTION)

def get_vlc_password():
    """"""
    return config.get(DEFAULT_SECTION, VLC_PASSWORD_OPTION)
    
def get_uri():
    """"""
    return config.get(DEFAULT_SECTION, URI_OPTION)
    
def get_url_history():
    """"""
    return json.loads(config.get(DEFAULT_SECTION, URL_HISTORY_OPTION))

def add_url_history(url):
    """"""
    url_list = get_url_history()
    if url in url_list:
        url_list.pop(url_list.index(url))
    else:
        if len(url_list) > 9:
            url_list.pop()
    url_list.insert(0, url)
    config.set(DEFAULT_SECTION, URLS_OPTION, json.dumps(url_list))
    fd = open(CONFIG_FILE, "w")
    config.write(fd)
    fd.close()

config = ConfigParser.SafeConfigParser(DEFAULTS)
config.read(CONFIG_FILE)

if __name__ == "__main__":
    print get_urls()
