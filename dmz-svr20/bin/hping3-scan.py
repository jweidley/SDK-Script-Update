#!/usr/bin/python3
# Purpose: Use Hping3 to generate traffic that will be blocked by vSRX screens.
# Version: 0.7
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 22Mar20: Fixed the -I interface options to be accurate.
# 0.3: 4Apr20: Add optional --continuous option
# 0.4: 18May20: Variabilized time option & increased to 15.
# 0.5: 23Aug20: Added IP Spoofing Attack
# 0.6: 2Sep20: Added IP spoofing to all attacks
# 0.7: 18Feb21: Added configuration via sdk.conf
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
svrInt = checkConfig(config, "dmz-svr", "int")
target = checkConfig(config, "script", "trustNet")
duration = checkConfig(config, "script", "duration")

################
# Variables
################
endTime = time() + 60 * duration

#
# counts: Used to randomize the number of packets in the attacks
counts = ["5", "7", "10", "12", "15", "20", "25"]

#
# spoofIPs: 
# List of foreign country IP addresses to spoof scans from. All IPs 
# have a 4th octet of .99 so when you are looking at the logs you know that
# it was this script that generated that traffic.
# Source: https://lite.ip2location.com/ip-address-ranges-by-country
# NOTE: The GeoIP DB on Space is kind old so it may not always match.
spoofIPs = [
		"1.1.1.99",             # AU
		"202.202.202.99",	# CN
		"14.192.60.99",		# CN
		"5.83.16.99",		# Ukraine
		"5.101.44.99",		# Germany
		"5.255.30.99",		# Yeman
		"41.74.32.99",		# Chad
		"41.75.64.99",		# Congo
		"5.8.64.99"             # RU
	]

attackCommands = [
        "sudo hping3 -q --fast --icmp -d 1000 -c ",
        "sudo hping3 -q --fast -p 22 -c ",
        "sudo hping3 -q --fast -S -c ",
        "sudo hping3 -q --fast --lsrr 192.168.99.1 --syn -p 22 -c ",
        "sudo hping3 -q --fast --rroute --syn -p 22 -c ",
        "sudo hping3 -q --fast --ssrr 192.168.99.1 --syn -p 22 -c ",
        "sudo hping3 -q --fast --fin -p 22 -c ",
        "sudo hping3 -q --fast -p 22 --syn --fin -c "
        ]

################
# Main
################
parser = argparse.ArgumentParser(description='Run an hping3 scan to generate SCREEN alarms on vSRX.')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    while args.continuous:
        genCommand = choice(attackCommands) + choice(counts) + " -I " + svrInt + " --rand-dest " + target + " --spoof " + choice(spoofIPs)
        system(genCommand)
        sleep(10)
else:
    print("############################################################################################")
    print(" Running SCREENS Scan for " + str(duration) + " minutes")
    print("############################################################################################")
    while time() < endTime:
        genCommand = choice(attackCommands) + choice(counts) + " -I " + svrInt + " --rand-dest " + target + " --spoof " + choice(spoofIPs)
        print("Using attack command: " + genCommand)
        system(genCommand)
        print("================= Sleeping....")
        sleep(10)

## End of Script ##
