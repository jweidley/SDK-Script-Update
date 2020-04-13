#!/usr/bin/python3
# Purpose: Generate traffic to sites blocked by vSRX EWF
# Verion: 0.1
##########################################################################################
# ChangeLog:
# 0.1: 10Apr20: Initial release
##########################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from os import system
import argparse

################
# Variables
################
endTime = time() + 60 * 5
wget = "/usr/bin/wget -q -O /dev/null "
urls = [
	"https://www.legalsportsreport.com/sports-betting/",
	"https://mybookie.ag/sportsbook/",
	"https://www.sportsbetting.ag/",
	"https://www.sportsbettingdime.com/",
	"https://www.glassdoor.com/Job/boston-jobs-SRCH_IL.0,6_IC1154532.htm",
	"https://www.monster.com/jobs/l-boston-ma",
	"https://www.oddsshark.com/sportsbook-review"
	]
sleepTimes = [ 1, 2, 5, 10, 12, 15]

################
# Main
################
parser = argparse.ArgumentParser(description='Generate traffic to sites blocked by vSRX EWF')
parser.add_argument("--continuous", action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    print("Continuous Enabled")
    print("=================================================================")
    print("  EWF Traffic Generator --continuous")
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
    print("Continuous NOT Enabled")
    print("=================================================================")
    print("  EWF Traffic Generator")
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
