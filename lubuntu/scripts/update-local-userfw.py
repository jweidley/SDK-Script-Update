#!/usr/bin/python3
# Purpose: Add information to the local user auth table on SRX
# Version: 0.3
#
############################################################################################################
# CHANGELOG:
# - 0.1: Initial Release
# - 0.2: Fix for "RpcError(severity: error, bad_element: None, message: "This record has been in user-identification 
#	local-authentication-table.")" error. See note 2 below.
# - 0.3: 22Mar20: Fix first run condition where the localAuthTable on the vSRX is NULL.
#
############################################################################################################
# NOTES:
# 1. You can NOT specify more than 1 role in a single 'add' API call. Space, comma, and space comman
#	doesnt work.
# 2. From the cli you can re-add lines but from the API you can NOT overwrite an existing entry. NEED to
#	delete the first entry.
#
############################################################################################################

################
# Modules
################
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
# Firewall Variables
user = "juniper"
passwd = "juniper123"
vsrx = "192.168.100.1"
dev = Device(host=vsrx,gather_facts='False',user=user,password=passwd)

# User Auth Variables
currentUser = getuser()
host_ip = "192.168.100.10"

if currentUser == "demo-user":
	roles = "Tier1"
else:
	roles = "Tier3"

################
# Functions
################

def removeAdd(dev):
	print("- Removing existing host entry...")
	cmd = dev.rpc.request_userfw_local_auth_table_delete_ip(ip_address=host_ip)

	print("- Adding New UserFW Entry...")
	print("  + Adding Role Users")
	cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles="Users")

	print("  + Adding User Specific Role")
	cmd2 = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles=roles)

def justAdd(dev):
	print("- Adding New UserFW Entry...")
	print("  + Adding Role Users")
	cmd = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles="Users")

	print("  + Adding User Specific Role")
	cmd2 = dev.rpc.request_userfw_local_auth_table_add(user_name=currentUser,ip_address=host_ip,roles=roles)

################
# Main
################
print("=================================================================")
print("   SRX UserFW Login ")
print("=================================================================")

# Make connection to the vSRX and pull the local auth table
try:
	dev.open()
	look = dev.rpc.get_userfw_local_auth_table_all({'format':'text'})

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
print("!!....Completed Successfully...!!")
sleep(3)

## End of Script ##
