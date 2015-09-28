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

import os
import pwd
import atexit
import logging
import subprocess

import config

from threading import Thread
from pyalsa import alsamixer

class SoundControl:
    """"""
    VOL = [0, 19, 30, 38, 44, 48, 52, 56, 59, 62, 64]
    ELEMENT = config.get_element()

    def __init__(self):
        """"""
        mixer = alsamixer.Mixer()
        mixer.attach()
        mixer.load()
        #print mixer.list()
        self.element = alsamixer.Element(mixer, self.ELEMENT)
        #print self.element.get_volume_range()
        
    def _get_index(self):
        """"""
        vol = self.element.get_volume()
        cont = 0
        for i in self.VOL:
            if i < vol:
                cont += 1
            else:
                break
        return cont

    def get_mute(self):
        """"""
        return not self.element.get_switch()

    def toggle_mute(self):
        """"""        
        self.element.set_switch_all(self.get_mute())

    def get_volume(self):
        """"""
        return self._get_index()*10

    def volume_up(self):
        """"""
        i = self._get_index()
        if i < 10:
            self.element.set_volume_all(self.VOL[i+1])

    def volume_down(self):
        """"""
        i = self._get_index()
        if i > 0:
            self.element.set_volume_all(self.VOL[i-1])
            
class ProcessManager:
    """"""
    USER = config.get_user()
    
    UPTIME_CMD = ["uptime"]
    UNAME_CMD = ["uname", "-a"]
    SUSPEND_CMD = ["pm-suspend"]
    VLC_CMD = ["/usr/bin/vlc", "-I", "http", "--http-password", config.get_vlc_password(), 
    "--x11-display", ":0", "--fullscreen"]
    
    VLC_LOG = "/tmp/musicbox_vlc.log"
    
    def __init__(self):
        """"""
        pwd_record = pwd.getpwnam(self.USER)
        self.uid = pwd_record.pw_uid
        self.gid = pwd_record.pw_gid
        self.env = os.environ.copy()
        self.env["USER"] = pwd_record.pw_name
        self.env["HOME"] = pwd_record.pw_dir
        self.env["LOGNAME"] = pwd_record.pw_name
        
        format = logging.Formatter("%(asctime)s %(name)s: %(message)s")
        
        self.vlc_logger = logging.getLogger("VLC")
        self.vlc_logger.setLevel(logging.INFO)
        log = logging.FileHandler(self.VLC_LOG, "w")
        log.setFormatter(format)
        self.vlc_logger.addHandler(log)
                
        self.buffers = []
        
        self.vlc = self._spawn(self.VLC_CMD)
        if self.vlc:
            th = Thread(target=self.vlc_log_buffer)
            th.daemon = True
            th.start()
            self.buffers.append(th)
        
        atexit.register(self.quit)
        
    def _demote(self):
        """"""
        os.initgroups(self.USER, self.gid)
        os.setuid(self.uid)
        
    def _spawn(self, cmd):
        """"""
        try:
            p = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                preexec_fn=self._demote,
                env=self.env)
        except Exception as e:
            print " ".join(cmd), e
        else:
            return p

    def suspend(self):
        """"""
        try:
            p = subprocess.Popen(self.SUSPEND_CMD)
        except Exception as e:
            print e
        else:
            return True

    def get_uname(self):
        """"""
        p = self._spawn(self.UNAME_CMD)
        if p:
            return p.communicate()[0].strip()

    def get_uptime(self):
        """"""
        p = self._spawn(self.UPTIME_CMD)
        if p:
            return p.communicate()[0].strip()
        
    def restart_vlc(self):
        """"""
        try:
            self.vlc.terminate()
            self.vlc.wait()
        except Exception as e:
            self.vlc_logger.error(e)
        else:
            self.vlc_logger.warning("Restarted")
            self.vlc = self._spawn(self.VLC_CMD)
        
    def get_vlc_log(self, full=False):
        """"""
        f = open(self.VLC_LOG, "r")
        tmp = f.readlines()
        f.close()
        if full:
            return "".join(tmp)
        else:
            return "".join(tmp[-20:])
            
    def vlc_log_buffer(self):
        """"""
        while True:
            line = self.vlc.stdout.readline()
            if line:
                self.vlc_logger.info(line.strip())
        
    def quit(self):
        """"""
        for p in [self.vlc]:
            try:
                if p:
                    p.terminate()
            except Exception as e:
                print e
        for th in self.buffers:
            th.join(0.1)

if __name__ == "__main__":
    p = ProcessManager()
