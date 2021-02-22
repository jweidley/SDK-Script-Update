#!/usr/bin/python3
# Purpose: Periodically switch users in the SRX auth table so traffic appears to be generated from different
#           users.
# Version: 0.2
#
############################################################################################################
# CHANGELOG:
# - 0.1: 18Sep20: Initial Release
# - 0.2: 1Jan21: Added configuration via sdk.conf
############################################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
from lxml import etree
from sdkModules import *
from getpass import getuser
from time import sleep
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectTimeoutError
import re
import argparse
import sys

################
# SDK Config
################
# Read SDK configuration file
config = readConfig()

# Check if all required options are configured
srxCreds = checkConfigSRX(config, "vsrx")

# Get Lubuntu IP from config file
host_ip = checkConfig(config, "lubuntu", "ip")

################
# Variables
################
# Create connection to vSRX
dev = Device(host=srxCreds['vsrx'],gather_facts='False',user=srxCreds['user'],password=srxCreds['passwd'])

# User Variables
users = [                   # List of usernames to switch between
        "jsmith",
        "bjones",
        "abrown",
        "bwhite",
        "cpeterson"
    ]

switchTime = [180,300,600]  # Time (in seconds) between switching users.
roles = "Sales"             # Role to apply to users


################
# Functions
################
def removeAdd(dev):
    currentUser = choice(users)
    print("- Removing existing host entry...")
    cmd = dev.rpc.request_userfw_local_auth_table_delete_ip(ip_address=host_ip)

    print("- Adding New UserFW Entry for " + currentUser)
    cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles="Users")
    cmd2 = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles=roles)

def justAdd(dev):
    currentUser = choice(users)
    print("- Adding New UserFW Entry...")
    cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles="Users")
    cmd2 = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles=roles)

################
# Main
################
parser = argparse.ArgumentParser(description='UserFW user switcher')
parser.add_argument("--continuous", required=True, action='store_true', help="Run script continuously")
args = parser.parse_args()

if args.continuous:
    print("=================================================================")
    print("   UserFW User Switcher")
    print("=================================================================")

    while args.continuous:
    # Make connection to the vSRX and pull the local auth table
        try:
            dev.open()
            look = dev.rpc.get_userfw_local_auth_table_all({'format':'text'})

            # Find null auth table condition (common with first run UserFW)
            if look is True:
        	    print("First Run Condition...")
        	    justAdd(dev)
            else:
	            # Format and find the number of auth table entries
	            formatted = etree.tostring(look)
	            decoded = formatted.decode('utf-8') ## Converts bytes-like to string
	
	            # The output is multiline so we need to search for the total number of auth entries in the output
	            match = re.search(r'^Total\sentries:\s\d+', decoded, re.MULTILINE)
	            totalLine = re.split('\s+', match.group(0))

	            # Decide what to do based on results
	            if int(totalLine[2]) > 0:
	    	        print("Auth table entries found: deleting and adding...")
	    	        removeAdd(dev)
	            else:
	    	        print("No Auth Table entries found: adding...")
	    	        justAdd(dev)

            # Exit
            dev.close()
            waitTime = choice(switchTime)
            print("...Waiting for " + str(waitTime) + " seconds...\n")
            sleep(waitTime)

        except ConnectError as err:
            print("!!..The vSRX appears to be down..!!")
            print("Cannot connect to device: {0}".format(err))
            sleep(3)
            sys.exit(1)

        except Exception as err:
    	    print("!!..The vSRX appears to be down..!!")
    	    print(err)
    	    sleep(3)
    	    sys.exit(1)

        except KeyboardInterrupt:
            print("-- Manually Exiting Program.")
            raise SystemExit

## End of Script ##
