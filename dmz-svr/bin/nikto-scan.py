#!/usr/bin/python3
# Purpose: Run Nikto scans to generate IPS alerts on vSRX
# Details: The script will run for 5 minutes and randomly generate the Tuning level.
# Version: 0.2
#######################################################################

################
# Modules
################
from time import time, sleep
from random import choice
from os import system

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

