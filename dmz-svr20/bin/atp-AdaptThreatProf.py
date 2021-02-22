#!/usr/bin/python3
# Purpose: Generate traffic to trigger Adaptive Threat Profiling blocks
# Version: 0.2
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: 14Oct20: Initial Release
# 0.2: 20Oct20: Modularize and clean up
######################################################################################

################
# Modules
################
from time import time, sleep
from random import choice
from os import system

################
# Variables
################
wgetIdpCmd = "/usr/bin/wget -q -O /dev/null --connect-timeout=3 --tries 1 http://192.168.100.20/%252E%252E%252F/etc/passwd --bind-address "
wgetProfCmd = "/usr/bin/wget -q -O /dev/null --timeout=10 --tries 1 --no-check-certificate --bind-address "
idpAttkSrc = ["192.168.200.30", "192.168.200.31", "192.168.200.40", "192.168.200.41"]
profSrc = ["192.168.200.20 https://www.tor2web.org", "192.168.200.21 https://www.megaproxy.com"]

################
# Main
################
print("############################################################################################")
print(" Generating IDP Attack Traffic")
print("############################################################################################")

for ip in idpAttkSrc:
	print("   " + wgetIdpCmd + " " + ip)
	system(wgetIdpCmd + " " + ip)
	print("   -- Sleeping for 5 seconds")
	sleep(5)
	
print(" ")
print("############################################################################################")
print(" Generating Suspicious Traffic")
print("############################################################################################")

for ip in profSrc:
	print("   " + wgetProfCmd + " " + ip)
	system(wgetProfCmd + " " + ip)
	print("   -- Sleeping for 5 seconds")
	sleep(5)


print(" ")
print("========== COMPLETED! ===========")
sleep(10)

## End of Script ##
