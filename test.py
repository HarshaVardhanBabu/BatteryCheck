#!/usr/bin/env python
"""test.py: Notify the user when the battery is charged over 90% and discharging below 20%"""

__author__      = "Harsha Vardhan Babu"
__copyright__   = "Copyright 2014"

import commands
import pynotify
import time, threading
import os

MAX_LEVEL = 90
MIN_LEVEL = 20

def checkBatPercentage():#check the battery level using awk script
	percentage = (commands.getoutput("acpi | awk '{print $4}'"))
	percentint = int(percentage[:-2])
	return percentint

def checkBatStatus():#checks whether battery is charging or discharging
	return (commands.getoutput("acpi | awk '{print $3}'"))[:-1]

def notifyUser(msg):#native notifications
	pynotify.init(msg)
	notification = pynotify.Notification("Battery "+checkBatStatus()+" "+str(checkBatPercentage())+"%"+msg)
	notification.show()
	os.system('mplayer "$HOME/Documents/BatteryCheck/test.wav"') #absolute path for the music file
	return None

def Result():
	if(checkBatStatus() == "Charging") and (checkBatPercentage() >= MAX_LEVEL):
		return "Unplug AC power !!"
	elif(checkBatStatus() == "Discharging") and (checkBatPercentage() <= MIN_LEVEL):
		return "Plug AC power !!"
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
