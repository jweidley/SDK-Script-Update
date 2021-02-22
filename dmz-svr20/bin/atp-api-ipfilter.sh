#!/bin/bash
# Purpose: Process a sample web server log to gather source addresses and update ATP Cloud
#	   IPFilter list.
# Author: John Weidley (Sample code provided by Craig Dods, Michael Bergt)
# Version: 0.2
#################################################################################################
# ChangeLog
# 0.1: 5Jan21: Initial Release
# 0.2: 8Jan21: added better error checking on API calls
#################################################################################################

##########################
# Variables
##########################
# API Token that was generated in the ATP cloud WebUI (Administration > Application Tokens)
# The token from ATP Cloud should be inside the double quotes in 1 continuous line.
APPToken="ADD-YOUR-TOKEN-HERE"

# Feed name that was configured in the ATP cloud WebUI (Configure > Adaptive Threat Profiling)
BlockFeed="Recommended_IP_Blocks"

# Web Server sample log file
webSvrLog=/usr/local/bin/webserver.log

# Local file that contains
blockList=/tmp/blockList.txt

################################################################
# curlWithStatus: Run specific curl command with the options to
#	see the status code and message.
################################################################
curlWithStatus() {
	code=0
	statuscode=0
	body=0

	# Determine whether to run the delete or add
	if [ $1 == "delete" ]; then
		statuscode=$(curl -s -k -w "%{http_code}" -XDELETE -H "Authorization: Bearer $APPToken" -F server='*' \
			-o >(cat >/tmp/curl_body) \
			"https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/ipfilter/param/${BlockFeed}"
			) || code="$?"
	elif [ $1 == "add" ]; then
		statuscode=$(curl -s -k -w "%{http_code}" -XPOST -H "Authorization: Bearer $APPToken" -F file=@${blockList} \
			-o >(cat >/tmp/curl_body) \
			"https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/ipfilter/file/${BlockFeed}"
			) || code="$?"
	else
		echo "ERROR: Unknown error...exiting!"
	fi

	body="$(cat /tmp/curl_body)"
	#echo "statuscode : $statuscode"
	#echo "exitcode : $code"
	#echo "body : $body"

	#####################################
	# Check/Report status
	# ! May not be 100% complete
	#####################################
	if [ $statuscode == "404" ]; then
		echo "   + Feed not present (HTTP: $statuscode)...continuing"
	elif [ $statuscode == "200" ] || [ $statuscode == "202" ]; then
		echo "   + Feed operation successful. (HTTP: $statuscode)...continuing"
		echo "   + Message: $body"
	else
		echo "   ---------------------------------------------------"
		echo "   ERROR: Feed Update failed with error:"
		echo "     - Status Code: $statuscode"
		echo "     - $body"
		echo "   ---------------------------------------------------"
		echo " "
		echo "    Troubleshooting:"
		echo "    1. Ensure the APPToken variable is formatted correctly in the script"
		echo "    2. Ensure the Application Token is still 'active' in ATP Cloud"
		echo " "
		echo "...Exiting..."
		exit
	fi
}

##########################
# Main
##########################
clear
echo "========================================================================"
echo " ATP API Feed Update demo"
echo "========================================================================"

# Sanity check APPToken variable
if [ $APPToken == "ADD-YOUR-TOKEN-HERE" ]; then
	echo "ERROR: The APPToken variable hasn't been set!"
	echo "  - Go to ATP Cloud WebUI (Administration > Application Tokens) to generate one"
	echo "  - Add Token to /usr/local/bin/atp-api-ipfilter.sh script"
	sleep 10
	exit
fi

# Check if webserver.log exists
if [ -f $webSvrLog ]; then
	echo "- Creating blocklist from webserver log..."
	cat $webSvrLog | awk '{print $1}' | sort -n | uniq > $blockList
else
	echo "ERROR: !! $webSvrLog is MISSING....Exiting!!"
	exit
fi

sleep 5

echo "- Deleting feed contents from ATP Cloud..."
curlWithStatus delete

sleep 10

echo "- Updating feed contents in ATP Cloud..."
curlWithStatus add

sleep 2

# Clean up temporary file
rm $blockList

echo "-- COMPLETE: Feed Successfully Update!!"
sleep 5

## End of script #
