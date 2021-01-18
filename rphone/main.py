# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from Deal_log import Deal_log
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

def file_walk(fold):
    file_names = []
    files = os.listdir(fold)
    for f in files:
        f_d = os.path.join(fold,f)
        if os.path.isdir(f_d):
            file_walk(f_d)
        else:
            file_names.append(os.path.join(fold,f_d))
    return file_names

def process_file(fold):
    # Use a breakpoint in the code line below to debug your script.
    files_list = file_walk(fold)
    deal_log = Deal_log("deal_log")
    failed_monkey = "F_Monkey.txt"
    failed_logcat = "F_Logcat.txt"
    str1 = "_monkey"
    str2 = "_logcat"

    for file in files_list:
        if str1 in file:
            monkey = deal_log.deal_monkey(file)
            filename = os.path.basename(file)
            apkname = os.path.splitext(filename)[0].replace("_monkey","")
            if monkey == 3:
                with open(failed_monkey, 'a') as wf:
                    wf.write(apkname+"\tsuccess\n")
            else:
                with open(failed_monkey, 'a') as wf:
                    wf.write(apkname+"\tfailed\n")
    #count all crash
        elif str2 in file:
            logcat = deal_log.deal_logcat(file)
            filename = os.path.basename(file)
            apkname = os.path.splitext(filename)[0].replace("_logcat", "")
            if logcat == -1:
                with open(failed_logcat, 'a') as wf:
                    wf.write(apkname + "\tfailed\n")
            else:
                with open(failed_logcat, 'a') as wf:
                    wf.write(apkname + "\tsuccess\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   #process_file("/Users/gongliangyi/Documents/Emulation_crash/pythonProject/XiaomiLog/")
   test_all_apks()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
