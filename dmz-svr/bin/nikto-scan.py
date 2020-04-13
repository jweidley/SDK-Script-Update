#!/usr/bin/python3
# Purpose: Run Nikto scans to generate IPS alerts on vSRX
# Version: 0.3
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 20Mar20: Added addition tuning levels
# 0.3: 4Apr20: Add optional --continuous option
######################################################################################

################
# Modules
################
from time import time, sleep
from random import choice
from os import system
import argparse

################
# Variables
################
endTime = time() + 60 * 5
nikto = "/usr/bin/nikto"
target = "192.168.100.20"
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
    print(" Running Nikto Scan for 15 minutes")
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
