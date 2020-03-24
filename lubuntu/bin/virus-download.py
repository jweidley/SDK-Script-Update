#!/usr/bin/python3
# Purpose: Continuously download versions of the EICAR test virus from the dmz-svr vhosts to generate logs on SRX
# Verion: 0.3
##########################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from os import system

################
# Variables
################
endTime = time() + 60 * 5
w3m = "/usr/bin/w3m"
url = ["http://192.168.200.20/", "http://192.168.200.30/", "http://192.168.200.40/"]
viri = ["eicar_com.zip", "eicarcom2.zip"]
sleepTimes = [ 1, 5, 10, 15, 20]

################
# Main
################
while time() < endTime:
	genURL = w3m + " " + choice(url) + choice(viri) + " -dump"
	print("==============================================")
	print(" URL: " + genURL)
	print("==============================================")
	system(genURL)
	sleepfor = choice(sleepTimes)
	print("Sleeping for " + str(sleepfor) + " seconds...")
	sleep(sleepfor)
	print

## End of Script ## 
