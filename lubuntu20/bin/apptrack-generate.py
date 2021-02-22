#!/usr/bin/python3
# Purpose: Generate traffic to sites to generate traffic for AppTrack
# Verion: 0.4
##########################################################################################
# ChangeLog:
# 0.1: 15Apr20: Initial release
# 0.2: 22May20: Variabilize time option
# 0.3: 4Jun20: Added amazon & fb/juniper twice for AppFW testing
# 0.4: 24Jan21: Added configuration via sdk.conf
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
duration = checkConfig(config, "script", "duration")


################
# Variables
################
endTime = time() + 60 * duration
wget = "/usr/bin/wget -q -O /dev/null --no-check-certificate "
urls = [
	"youtube.com",
	"outlook.com",
	"www.facebook.com/JuniperNetworks/",
	"www.facebook.com/JuniperNetworks/",
	"linkedin.com",
	"yahoo.com",
	"tumblr.com",
	"twitter.com",
	"https://player.vimeo.com/video/252767901",
	"cnn.com",
	"cnet.com",
	"amazon.com",
	"amazon.com",
	"reddit.com",
	"espn.com",
	"wikipedia.org",
	"apple.org",
	"juniper.net"
	]
sleepTimes = [ 1, 2, 3, 1, 2, 1]

################
# Main
################
parser = argparse.ArgumentParser(description='Generate traffic to sites for AppTrack')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    print("=================================================================")
    print("  AppTrack Traffic Generator --continuous")
    print("=================================================================")
    while args.continuous:
        site = choice(urls)
        genURL = wget + site
        print(" - URL: " + site)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print
else:
    print("=================================================================")
    print("  AppTrack Traffic Generator: " + str(duration) + " minutes")
    print("=================================================================")
    while time() < endTime:
        site = choice(urls)
        genURL = wget + site
        print(" - URL: " + site)
        system(genURL)
        sleepfor = choice(sleepTimes)
        print("    Sleeping for " + str(sleepfor) + " seconds...")
        sleep(sleepfor)
        print

## End of Script ##
