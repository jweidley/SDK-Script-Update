#!/usr/bin/python3
# Purpose: Download files with restricted extensions
# Verion: 0.5
##########################################################################################
# ChangeLog:
# 0.1: initial release
# 0.2: added 5 minute stop timer
# 0.3: 4Apr20: Added optional --continuous option
# 0.4: 22May20: Variabilize time option
# 0.5: 1Jan21: Added configuration via sdk.conf
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
# Read SDK configuration file
config = readConfig()

# Get config values
destinations = checkConfig(config, "dmz-svr", "http_svrs")
duration = checkConfig(config, "script", "duration")

################
# Variables
################
endTime = time() + 60 * duration
wget = "/usr/bin/wget -q -O /dev/null "
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
        site = choice(destinations)
        file = choice(files)
        genURL = wget + "http://" + site + "/" + file
        print(" - URL: " + "http://" + site + "/" + file)
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
        site = choice(destinations)
        file = choice(files)
        genURL = wget + "http://" + site + "/" + file
        print(" - URL: " + "http://" + site + "/" + file)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print

## End of Script ##
