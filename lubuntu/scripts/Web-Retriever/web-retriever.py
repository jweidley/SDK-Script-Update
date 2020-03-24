#!/usr/bin/python3
# Purpose: Continuously access a website to test failover via SRX RPM pseudo SLB
# Verion: 0.3
##########################################################################################

###################################
# Modules
###################################
from time import time,sleep
from random import choice
from os import system
import datetime

###################################
# Variables
###################################
wget = "/usr/bin/wget"
preOptions = '--tries=2 --connect-timeout=2 -qO-'
postOptions = '| grep svr10'
url = "http://192.168.100.100/"
sleepTime = int("1")

###################################
# Main
###################################
while True:
	# Get date/time & format
	now = datetime.datetime.now()
	timeStamp = now.strftime("%H:%M:%S")

	# Build URL
	genURL = wget + " " + preOptions + " " + url + " " + postOptions

	# Execute
	print(timeStamp)
	system(genURL)
	print("Sleeping for " + str(sleepTime) + " seconds...")
	sleep(sleepTime)
	print

## End of Script ## 
