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
