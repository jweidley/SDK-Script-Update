#!/usr/bin/python3
# Purpose: Run Nikto scans to generate IPS alerts on vSRX
# Version: 0.1 (SD Cloud Demo environment)
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
######################################################################################
# TODO
# 1. need to add NAT stuff to the continuous condition
# 2. merge the regular script with multi (this one) and provide options??
######################################################################################

################
# Modules
################
from time import time, sleep
from random import choice
from os import system
import argparse
import signal
import sys

################
# Functions
################
def signal_handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? "
    print(msg, end="", flush=True)
    res = input("y/n")
    if res == 'y':
       print("  ! Clearing NAT rules....")
       system("sudo iptables -t nat --delete POSTROUTING 1")
       exit(1)
    else:
       print("Ok, resuming scan...")

# Starting signhandler
signal.signal(signal.SIGINT, signal_handler)  # Register the signal to trap


################
# Variables
################
duration = 15
endTime = time() + 60 * duration
nikto = "/usr/bin/nikto"
#target = "192.168.100.20"
targets = ["192.168.100.20", "10.16.10.10", "10.16.20.10", "192.168.100.20", "10.16.30.10"]
sources = ["192.168.200.21", "192.168.200.31", "192.168.200.41"]
tuning = ["7", "8", "7", "x"]

################
# Main
################
parser = argparse.ArgumentParser(description='Run an Nikto scan to generate IDP alerts on vSRX.')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    while args.continuous:
        scanCommand = nikto + " -host " + choice(targets) + " -Tuning " + choice(tuning)
        system(scanCommand)
        sleep(60)

else:
    print("############################################################################################")
    print(time())
    print(endTime)
    print(time() - endTime)
    print(" Running IDP Scan for " + str(duration) + " minutes")
    print("############################################################################################")
    while time() < endTime:
        scanCommand = nikto + " -host " + choice(targets) + " -Tuning " + choice(tuning)
        newSource = choice(sources)
        print("======================================================")
        print("== Source IP: " + newSource)
        print("== Command: " + scanCommand)
        print("======================================================")
        
        #####################################################################
        # Source NAT: iptables packet mangling
        #####################################################################
        print("- Removing NAT...")
        # use: "iptables -t nat -L -n -v --line-number" to see NAT rules
        system("sudo iptables -t nat --delete POSTROUTING 1")
        print("- Setting Source NAT..." + newSource)
        system("sudo iptables -t nat -A POSTROUTING -o ens3.200 -s 192.168.200.10 -p tcp --dport 80 -j SNAT --to " + newSource)
        #### End packet mangling ####

        system(scanCommand)
        print("================= Sleeping....")
        sleep(60)

## End of script ##
