#!/usr/bin/python3
# Purpose: Start iPerf Server
# Version: 0.1
# Author: John Weidley
######################################################################################
# ChangeLog:
# 0.1: Initial Release
######################################################################################

################
# Modules
################
from time import time, sleep
from random import choice
from os import system

################
# Main
################
print("############################################################################################")
print(" iPerf Server")
print("############################################################################################")
command = "/usr/bin/iperf -s -i 1"
system(command)

## End of Script ##
