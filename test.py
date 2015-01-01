#!/usr/bin/env python

import commands
import pynotify
import time, threading
import os

def checkBatPercentage():
	percentage = (commands.getoutput("acpi | awk '{print $4}'"))
	percentint = int(percentage[:-2])
	return percentint

def checkBatStatus():
	return (commands.getoutput("acpi | awk '{print $3}'"))[:-1]

def notifyUser(msg):
	pynotify.init(msg)
	notification = pynotify.Notification("Battery "+checkBatStatus()+" "+str(checkBatPercentage())+"%"+msg)
	notification.show()
	os.system('mplayer "/home/harshavardhanbabu/Documents/BatteryCheck/test.wav"')
	return None

def Result():
	if(checkBatStatus() == "Charging") and (checkBatPercentage() >= 90):
		return "Unplug AC power !!"
	elif(checkBatStatus() == "Discharging") and (checkBatPercentage() <= 20):
		return "plug AC power !!"
	else:
		return "None"


def runForever():
	if(Result() == "Unplug AC power !!") or (Result() == "plug AC power !!"):
		notifyUser(Result())

def run():
	runForever()
	if (checkBatStatus() == "Discharging"):
		os.system("xbacklight -set "+str(checkBatPercentage())) # Adjust the brightness
	else:
		os.system("xbacklight -set 60") # set the brightness
	threading.Timer(300.0, run).start()

run()