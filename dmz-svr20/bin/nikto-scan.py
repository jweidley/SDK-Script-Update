#!/usr/bin/python3
# Purpose: Run Nikto scans to generate IPS alerts on vSRX
# Version: 0.5
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 20Mar20: Added addition tuning levels
# 0.3: 4Apr20: Add optional --continuous option
# 0.4: 18May20: Variabilize the time option & increased to 15
# 0.5: 18Feb21: Added configuration via sdk.conf
######################################################################################

################
# Modules
################
from time import time, sleep
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
target = checkConfig(config, "metasploitable", "ip")
duration = checkConfig(config, "script", "duration")

################
# Variables
################
endTime = time() + 60 * duration
nikto = "/usr/bin/nikto"
tuning = ["7", "8", "7", "x"]

################
# Main
################
parser = argparse.ArgumentParser(description='Run an Nikto scan to generate IDP alerts on vSRX.')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    while args.continuous:
        scanCommand = nikto + " -host " + target + " -Tuning " + choice(tuning)
        system(scanCommand)
        sleep(60)

else:
    print("############################################################################################")
    print(" Running IDP Scan for " + str(duration) + " minutes")
    print("############################################################################################")
    while time() < endTime:
        scanCommand = nikto + " -host " + target + " -Tuning " + choice(tuning)
        print("======================================================")
        print("== Command: " + scanCommand)
        print("======================================================")
        system(scanCommand)
        print("================= Sleeping....")
        sleep(60)

## End of script ##
