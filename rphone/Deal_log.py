# -*- coding: utf-8 -*-

import os
class Deal_log():
    def __init__(self,name):
        self.name = name

    def deal_monkey(self,filename):
        str1 = "Monkey aborted due to error"
        str3 = "Monkey finished"
        str2 = "No activities found to run, monkey aborted"
        with open(filename,'r') as fl:
            for line in fl.readline():
                if str1 in line:
                    return 1
                elif str2 in line:
                    return 2
                elif str3 in line:
                    return 3
                else:
                    return 0

    def deal_logcat(self,filename):
        str1 = "W/"
        str2 = "E/"
        str3 = "F/"
        str4 = "A/"
        aftfile = os.path.basename(filename)
        flag = 0
        # save crash file into a new file
        newfilename = "./Xiaomi_Crash/Crash_"+aftfile
        with open(newfilename,'a',encoding='utf-8') as wfl:
            with open(filename,'r',encoding='utf-8',errors='ignore') as fl:
                lines = fl.readlines()
                for line in lines:
                    if str2 in line:
                        wfl.write(line)
                        flag = 1
                    elif str3 in line:
                        wfl.write(line)
                        flag = 1
                    elif str1 in line:
                        flag = 1
                        continue
                    elif str4 in line:
                        flag = 1
                        wfl.write(line)
        if flag == 0:
            return -1
        else:
            return 0




