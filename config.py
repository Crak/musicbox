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

import ConfigParser

DEFAULT_SECTION = "DEFAULT"

HOST_OPTION = "host"
ELEMENT_OPTION = "element"
USER_OPTION = "user"
URI_OPTION = "uri"

DEFAULTS = {
    HOST_OPTION: "192.168.2.2",
    ELEMENT_OPTION: "Headphone",
    USER_OPTION: "musicbox",
    URI_OPTION: "file:///mnt/music"
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
    
def get_uri():
    """"""
    return config.get(DEFAULT_SECTION, URI_OPTION)

config = ConfigParser.SafeConfigParser(DEFAULTS)
config.read(CONFIG_FILE)

if __name__ == "__main__":
    config.write(open(CONFIG_FILE, "w"))
    print config.defaults()
