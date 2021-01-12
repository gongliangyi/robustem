# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:12:30 2020

@author: GLY
"""


import os
import sys
import time
from AdbManager import  AdbManager

file_name=[]

class ApkManager():
	def __init__(self, fold):
		self.fold = fold

	def file_walk(self,fold):
		files = os.listdir(fold)
		for fi in files:
			fi_d = os.path.join(fold,fi)
			if os.path.isdir(fi_d):
				self.file_walk(fi_d)
			else:
				file_name.append(os.path.join(fold,fi_d))
		return file_name

	def isCanInstall(self):
		# scan all apps in the fold, install them on the emulator and uninstall them one by one
		adbmanager = AdbManager()
		files_list = self.file_walk(self.fold)
		have_install = []
		with open("runAnd11APK.txt","r") as file:
			for line in file.readlines():
				items = line[:-1].split('\t',3)
				have_install.append(items[0])

		print(len(have_install))
		with open("runAnd11APK.txt","a") as file:
			for file_name in files_list:
				if file_name in have_install:
					continue
				install_name = file_name
				uninstall_name = os.path.basename(file_name).strip('.apk')
				cmd = "adb  -d install -g -t "+install_name
				try:
					install_result = adbmanager.adb_cmd(cmd).decode("utf-8")
				except:
					continue
				time.sleep(3)
				if install_result == str("Success\n"):
					cmd = "adb  -d uninstall "+uninstall_name
					try:
						uninstall_result = (adbmanager.adb_cmd(cmd).decode("utf-8"))
					except:
						continue
					time.sleep(3)
					if uninstall_result == str("Success\n"):
						results = "Success\n"
					else:
						cmd = "adb  -d shell pm uninstall -k " + uninstall_name
						uninstall_result = (adbmanager.adb_cmd(cmd).decode("utf-8"))
						time.sleep(3)
				else:
					results = "Failure\n"
				file.write(install_name+"\t"+uninstall_name+"\t"+results)
				print(uninstall_name+"\t"+results)
		print(len(files_list))




