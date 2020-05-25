#!/usr/bin/python3
# Purpose: Download versions of the EICAR test virus from the dmz-svr
# Verion: 0.5
##########################################################################################
# ChangeLog:
# 0.1: Initial release
# 0.2: Download from dmz-svr and not from Internet (freaks out Corp IT)
# 0.3: Added download of zip version of virus
# 0.4: 4Apr20: Added optional --continuous option
# 0.5: 22May20: Variabilize time option
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
w3m = "/usr/bin/w3m"
urls = ["http://192.168.200.20/", 
        "http://192.168.200.30/", 
        "http://192.168.200.40/"
       ]
viri = ["eicar_com.zip", "eicarcom2.zip"]
sleepTimes = [ 1, 5, 10, 15, 20]

################
# Main
################
parser = argparse.ArgumentParser(description='Run a download of bad extensions for the SRX to block')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    print("=================================================================")
    print("  Virus Download --continuous")
    print("=================================================================")
    while args.continuous:
        site = choice(urls)
        file = choice(viri)
        genURL = w3m + " " + site + file + " -dump"
        print(" - URL: " + site + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print
else:
    print("=================================================================")
    print("  Virus Download: " + str(duration) + " minutes")
    print("=================================================================")
    while time() < endTime:
        site = choice(urls)
        file = choice(viri)
        genURL = w3m + " " + site + file + " -dump"
        print(" - URL: " + site + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print

## End of Script ## 
