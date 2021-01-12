# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:12:30 2020

@author: GLY
"""

import os
from AdbManager import AdbManager
from ApkManager import ApkManager
from ApkTest import ApkTest
import time
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def read_packname():
    apks = []
    with open("runAnd11APK.txt", "r") as file:
        for line in file.readlines():
            items = line[:-1].split('\t', 3)
            if items[2] == "Success":
                apks.append(items[0])
    return apks
# Press the green button in the gutter to run the script.
def test_all_apks():
    apks = read_packname()
    print(len(apks))
    for apk in apks:
        sapk = os.path.basename(apk).strip('.apk')

        logname = sapk+"_monkey.txt"
        if os.path.exists(logname):
            continue
          #  os.remove(logname)

        logcat = sapk+"_logcat.txt"
        #if os.path.exists(logcat):
           # os.remove(logcat)
        apktest = ApkTest(apk,logname,logcat)
        results = apktest.run_start()
        if results == "FFFF":
            print("Install Failed "+apk)
            break
        print("start packname "+sapk)
        apktest.run()
        print("ready to stop packname "+sapk)
        apktest.run_stop()
        time.sleep(2)

def test_uninstall_apk():
    apks = []
    with open("UApk.txt", "r") as file:
        for line in file.readlines():
            items = line[:-1].split(':', 2)
            apks.append(items[1])
    adb = AdbManager()
    for apk in apks:
        cmd = "adb  -d uninstall "+apk
        result = adb.adb_cmd(cmd)
        if result == "FFFF":
            print("uninstall "+apk+" failed")

def test_install_apk():
    apks = ApkManager("/home/system-pc/EmulatorCrash/Xiaomi/")
    apks.isCanInstall()

if __name__ == '__main__':
   # test_install_apk()
    test_all_apks()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
