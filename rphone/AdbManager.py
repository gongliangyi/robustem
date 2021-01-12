# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:12:30 2020

@author: GLY
"""

import os
import subprocess


class AdbManager():
    def __init__(self, packname="", logname="", logcat=""):
        self.packname = packname
        self.logname = logname
        self.logcat = logcat

    def adb_cmd(self, cmd):
        try:
            pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            return pi.stdout.read()
        except:
            return "FFFF"

    def adb_monkey(self, scheme="", total_events="50000", throttle="100"):
        logfile = self.logname
        packname = os.path.basename(self.packname).strip('.apk')
        if scheme == "random":
            cmd = "adb -d shell monkey -p " + packname + "--throttle " + throttle + " -s 1234 -v -v -v" + total_events + " >" + logfile
        elif scheme == "intellgent":
            cmd = "adb  -d shell monkey -p " + packname + " --throttle " + throttle  + " --pct-majornav 5 --pct-syskeys 2 --pct-touch 40 --pct-flip 13 --pct-motion 20 --pct-nav 5 --pct-appswitch 5 --pct-anyevent 10 --ignore-security-exception --kill-process-after-error --monitor-native-crashes -s 1234 -v -v -v" + total_events + " >" + logfile
        else:
            cmd = "adb  -d shell monkey -p " + packname + " --throttle " + throttle + " --pct-pinchzoom 2 --pct-rotation 2 --pct-syskeys 1 --kill-process-after-error --monitor-native-crashes -s 1234 -v -v -v  " + total_events + " >" + logfile
        return self.adb_cmd(cmd)

    def adb_install(self):
        packname = self.packname
        cmd = "adb  -d install -g  -t " + packname
        print(cmd)
        return self.adb_cmd(cmd)

    def adb_uninstall(self):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb  -d uninstall " + packname
        r = self.adb_cmd(cmd)
        print(cmd)
        if r != "FFFF":
            cmd = "adb  -d shell pm clear " + self.packname
            r = self.adb_cmd(cmd)
        return r

    def adb_kill(self):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb  -d shell am force-stop " + packname
        return self.adb_cmd(cmd)

    def adb_trim_mem(self, level="RUNNING_LOW"):
        # HIDDEN : release any UI objects that currently hold memory
        # RUNNING_MODERATE
        # RUNNING_LOW
        # RUNNING_CRITICAL : release any memory that your app doesn't need to run
        # COMPLETE, BACKGROUND<MODERATE : release as much memory as the process can
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb  -d shell pidof -s " + packname
        pid = self.adb_cmd(cmd)
        cmd_mem = "adb  -d shell am send-trim-memory " + pid + " " + level
        return self.adb_cmd(cmd_mem)

    def log_clear(self):
        cmd = "adb  -d logcat -c"
        return self.adb_cmd(cmd)

    def log_packname(self, level="W"):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb  -d logcat -b events -b system -b main '*:" + level + "' --pid='adb  -d shell pidof -s" + packname + "' -v time -v color -f " + self.logcat
        return self.adb_cmd(cmd)

    def log_all(self, level="W"):
        cmd = "adb  -d logcat -b events -b system -b main  *:" + level + " -v time -f /sdcard/" + self.logcat
        print(cmd+"\n")
        return self.adb_cmd(cmd)

    def log_delete(self):
        cmd = "adb  -d pull /sdcard/"+self.logcat
        self.adb_cmd(cmd)
        cmd = "adb  -d shell rm -r /sdcard/"+self.logcat
        return self.adb_cmd(cmd)

