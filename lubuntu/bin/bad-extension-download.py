#!/usr/bin/python3
# Purpose: Download files with restricted extensions
# Verion: 0.4
##########################################################################################
# ChangeLog:
# 0.1: initial release
# 0.2: added 5 minute stop timer
# 0.3: 4Apr20: Added optional --continuous option
# 0.4: 22May20: Variabilize time option
##########################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from os import system
import argparse

################
# Variables
################
duration = 15
endTime = time() + 60 * duration
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
parser = argparse.ArgumentParser(description='Run a download of bad extensions for the SRX to block')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    print("=================================================================")
    print("  Content Filter Test Script --continuous")
    print("=================================================================")
    while args.continuous:
        site = choice(urls)
        file = choice(files)
        genURL = wget + site + file
        print(" - URL: " + site + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print
else:
    print("=================================================================")
    print("  Content Filter Test Script: " + str(duration) + " minutes")
    print("=================================================================")
    while time() < endTime:
        site = choice(urls)
        file = choice(files)
        genURL = wget + site + file
        print(" - URL: " + site + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print

## End of Script ##
