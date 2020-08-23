#!/usr/bin/python3
# Purpose: Use Hping3 to generate traffic that will be blocked by vSRX screens.
# Version: 0.5
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 22Mar20: Fixed the -I interface options to be accurate.
# 0.3: 4Apr20: Add optional --continuous option
# 0.4: 18May20: Variabilized time option & increased to 15.
# 0.5: 23Aug20: Added IP Spoofing Attack
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
duration = 15
endTime = time() + 60 * duration
counts = ["5", "7", "10", "12", "15", "20", "25"]
attackCommands = [
        "sudo hping3 -q --fast --icmp -d 1000 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 -q --fast -p 22 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 -q --fast -S 192.168.100.10 -a 1.1.1.1 -c ",
        "sudo hping3 --lsrr 192.168.99.1 --syn -p 22 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 --rroute --syn -p 22 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 --ssrr 192.168.99.1 --syn -p 22 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 --fin -p 22 -I ens34.200 --rand-dest 192.168.100.x -c ",
        "sudo hping3 -q --fast -p 22 --syn --fin -I ens34.200 --rand-dest 192.168.100.x -c "
        ]

################
# Main
################
parser = argparse.ArgumentParser(description='Run an hping3 scan to generate SCREEN alarms on vSRX.')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    while args.continuous:
        genCommand = choice(attackCommands) + choice(counts)
        system(genCommand)
        sleep(10)
else:
    while time() < endTime:
        print("############################################################################################")
        print(" Running SCREENS Scan for " + str(duration) + " minutes")
        print("############################################################################################")
        genCommand = choice(attackCommands) + choice(counts)
        print("Using attack command: " + genCommand)
        system(genCommand)
        sleep(10)

## End of Script ##
