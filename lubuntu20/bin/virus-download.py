#!/usr/bin/python3
# Purpose: Download versions of the EICAR test virus from the dmz-svr
# Verion: 0.6
##########################################################################################
# ChangeLog:
# 0.1: Initial release
# 0.2: Download from dmz-svr and not from Internet (freaks out Corp IT)
# 0.3: Added download of zip version of virus
# 0.4: 4Apr20: Added optional --continuous option
# 0.5: 22May20: Variabilize time option
# 0.6: 1Jan21: Added configuration via sdk.conf
##########################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from os import system
from sdkModules import *
import argparse

################
# SDK Config
################
# Get destinations from config file
config = readConfig()

# Get config values
destinations = checkConfig(config, "dmz-svr", "http_svrs")
duration = checkConfig(config, "script", "duration")

################
# Variables
################
endTime = time() + 60 * duration
w3m = "/usr/bin/w3m"
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
        site = choice(destinations)
        file = choice(viri)
        genURL = w3m + " " + "http://" + site + "/" + file + " -dump"
        print(" - URL: " + "http://" + site + "/" + file)
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
        site = choice(destinations)
        file = choice(viri)
        genURL = w3m + " " + "http://" + site + "/" + file + " -dump"
        print(" - URL: " + "http://" + site + "/" + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print

## End of Script ## 
