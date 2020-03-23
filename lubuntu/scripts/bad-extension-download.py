#!/usr/bin/python3
# Purpose: Continuously download files with restricted extensions from dmz-svr
# Verion: 0.2
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
wget = "/usr/bin/wget -q -O /dev/null "
urls = [
	"http://192.168.200.20/",
	"http://192.168.200.30/",
	"http://192.168.200.40/"
	]
files = ["notepadpp.7z", "putty.exe", "winmerge.msi", "hosts.zip"]
sleepTimes = [ 1, 2, 5, 10, 12, 15]

################
# Main
################
print("=================================================================")
print("  Content Filter Test Script")
print("=================================================================")
while time() < endTime:
	genURL = wget + choice(urls) + choice(files)
	print("==============================================")
	print(" URL: " + genURL)
	print("==============================================")
	system(genURL)
	sleepfor = choice(sleepTimes)
	print("Sleeping for " + str(sleepfor) + " seconds...")
	sleep(sleepfor)
	print

## End of Script ##
