#!/usr/bin/python3
# Purpose: Periodically switch users in the SRX auth table so traffic appears to be generated from different
#           users.
# Version: 0.2
#
############################################################################################################
# CHANGELOG:
# - 0.1: 18Sep20: Initial Release
# - 0.2: 27Sep21: Added a function to eliminate repeated duplicate usernames & changed usernames
############################################################################################################

################
# Modules
################
from time import time,sleep
from random import choice
import argparse
import sys
from lxml import etree
import re
from getpass import getuser
from time import sleep
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectTimeoutError

################
# Variables
################

# SRX Variables
user = "juniper"
passwd = "juniper123"
vsrx = "192.168.100.1"
dev = Device(host=vsrx,gather_facts='False',user=user,password=passwd)

# User Variables
users = [                   # List of usernames to switch between
        "johns",
        "billj",
        "alisonb",
        "bettyw",
        "craigp"
    ]

switchTime = [180,240,300]  # Time (in seconds) between switching users.
host_ip = "192.168.100.10"  # IP of Lubuntu workstation
roles = "Sales"             # Role to apply to users
currentUser = ""

################
# Functions
################
def chooseUser(users,currentUser):
    while True:
        newUser = choice(users)

        if newUser != currentUser:
            break

    return newUser

def removeAdd(dev,currentUser):
    newUser = chooseUser(users,currentUser)
    print("- Removing existing host entry...")
    cmd = dev.rpc.request_userfw_local_auth_table_delete_ip(ip_address=host_ip)

    print("- Adding New UserFW Entry for " + newUser)
    cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=newUser,ip_address=host_ip,roles="Users")
    cmd2 = dev.rpc.request_userfw_local_auth_table_add(user_name=newUser,ip_address=host_ip,roles=roles)

    return newUser

def justAdd(dev,currentUser):
    newUser = chooseUser(users,currentUser)
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
        	    currentUser = justAdd(dev,currentUser)
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
	    	        currentUser = removeAdd(dev,currentUser)
	            else:
	    	        print("No Auth Table entries found: adding...")
	    	        currentUser = justAdd(dev,currentUser)

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
