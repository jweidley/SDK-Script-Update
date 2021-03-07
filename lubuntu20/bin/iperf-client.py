#!/usr/bin/python3
# Purpose: Start iPerf client
# Verion: 0.1
##########################################################################################
# ChangeLog:
# 0.1: Initial release
##########################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from os import system
from sdkModules import *

################
# SDK Config
################
# Get destinations from config file
config = readConfig()

# Get config values
server = checkConfig(config, "dmz-svr", "ip")

################
# Variables
################
iperf = "/usr/bin/iperf -i 1 -c "

################
# Main
################
print("=================================================================")
print("  iPerf Client: Generating traffic to " + server)
print("=================================================================")
command = iperf + server
system(command)

## End of Script ## 
