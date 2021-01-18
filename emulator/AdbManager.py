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
            cmd = "adb -e shell monkey -p " + packname + "--throttle " + throttle + " -s 1234 -v -v -v" + total_events + " >" + logfile
        elif scheme == "intellgent":
            cmd = "adb -e shell monkey -p " + packname + " --throttle " + throttle  + " --pct-majornav 5 --pct-syskeys 2 --pct-touch 40 --pct-flip 13 --pct-motion 20 --pct-nav 5 --pct-appswitch 5 --pct-anyevent 10 --ignore-security-exception --kill-process-after-error --monitor-native-crashes -s 1234 -v -v -v" + total_events + " >" + logfile
        else:
            cmd = "adb -e shell monkey -p " + packname + " --throttle " + throttle + " --pct-pinchzoom 2 --pct-rotation 2 --pct-syskeys 1 --kill-process-after-error --monitor-native-crashes -s 1234 -v -v -v  " + total_events + " >" + logfile
        return self.adb_cmd(cmd)

    def adb_fastbot(self, times = "5", throttle="100"):
        logfile = self.logname
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p "+packname +" --agent robot --running-minutes "+times+" --throttle "+throttle+" --ignore-crashes -v -v -v --bugreport "+ " > ./XiaomiLogs/" + logfile
        return self.adb_cmd(cmd)

    def adb_install(self):
        packname = self.packname
        cmd = "adb -e install -g  -t " + packname
        print(cmd)
        return self.adb_cmd(cmd)

    def adb_uninstall(self):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e uninstall " + packname
        r = self.adb_cmd(cmd)
        print(cmd)
        if r != "FFFF":
            cmd = "adb -e shell pm clear " + self.packname
            r = self.adb_cmd(cmd)
        return r

    def adb_kill(self):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e shell am force-stop " + packname
        return self.adb_cmd(cmd)

    def adb_trim_mem(self, level="RUNNING_LOW"):
        # HIDDEN : release any UI objects that currently hold memory
        # RUNNING_MODERATE
        # RUNNING_LOW
        # RUNNING_CRITICAL : release any memory that your app doesn't need to run
        # COMPLETE, BACKGROUND<MODERATE : release as much memory as the process can
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e shell pidof -s " + packname
        pid = self.adb_cmd(cmd)
        cmd_mem = "adb -e shell am send-trim-memory " + pid + " " + level
        return self.adb_cmd(cmd_mem)

    def log_clear(self):
        cmd = "adb -e logcat -c"
        return self.adb_cmd(cmd)

    def log_packname(self, level="W"):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e logcat -b events -b system -b main '*:" + level + "' --pid='adb -e shell pidof -s" + packname + "' -v time -v color -f " + self.logcat
        return self.adb_cmd(cmd)

    def log_all(self, level="W"):
        cmd = "adb -e logcat -b events -b system -b main  *:" + level + " -v time -f /sdcard/" + self.logcat
        print(cmd+"\n")
        return self.adb_cmd(cmd)

    def log_delete(self):
        cmd = "adb -e pull /sdcard/"+self.logcat+" ./XiaomiLogs/"+self.logcat
        self.adb_cmd(cmd)
        cmd = "adb -e shell rm -r /sdcard/"+self.logcat
        return self.adb_cmd(cmd)

    def fastbot_crashlog(self):
        packname = os.path.basename(self.packname).strip('.apk')
        cmd = "adb -e pull /sdcard/crash-dump.log ./XiaomiLogs/"+packname+"_dump.txt"
        self.adb_cmd(cmd)
        cmd = "adb -e pull /sdcard/oom-traces.log ./XiaomiLogs/"+packname+"_traces.txt"
        self.adb_cmd(cmd)
        cmd = "adb -e shell rm -rf /sdcard/crash-dump.log /sdcard/oom-traces.log"
        self.adb_cmd(cmd)

