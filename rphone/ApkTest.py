# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:12:30 2020

@author: GLY
"""

import os
import _thread
import time
from AdbManager import AdbManager
import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	try:
		tid = ctypes.c_long(tid)
		if not inspect.isclass(exctype):
			exctype = type(exctype)
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
		if res == 0:
			raise ValueError("invalid thread id")
		elif res != 1:
			# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
			ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
			raise SystemError("PyThreadState_SetAsyncExc failed")
	except:
		print("async_raise error")


def stop_thread(thread):
	"""
	@profile:强制停掉线程函数
	:param thread:
	:return:
	"""
	if thread == None:
		print('thread id is None, return....')
		return
	_async_raise(thread.ident, SystemExit)

def stop_logcat(adb):
	adb.log_delete()
	print("Logcat Delete Over...")

def run_logcat(adb):
	adb.log_clear()
	print("Logcat Clear...")
	adb.log_all()
	print("Logcat All over....")

def run_monkey(adb):
	adb.adb_monkey()
	print("Monkey Over....")




class ApkTest():
	def __init__(self, packname,logmonkey,logcat):
		self.pname = packname
		self.adb = AdbManager(packname,logmonkey,logcat)

	def run_start(self):
		return self.adb.adb_install()

	def run_stop(self):
		self.adb.adb_uninstall()


	def run(self):
		threads=[]
		monkey_pid = threading.Thread(target=run_monkey, args=(self.adb,))
		logcat_pid = threading.Thread(target=run_logcat, args=(self.adb,))

		logcat_pid.start()
		monkey_pid.start()
		monkey_pid.join()
		stop_logcat(self.adb)
		stop_thread(logcat_pid)
		print("apktest over....")

