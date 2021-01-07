#!/bin/bash
# Purpose: Process a sample web server log to gather source addresses and update ATP Cloud
#	   IPFilter list.
# Author: John Weidley (Sample code provided by Craig Dods, Michael Bergt)
# Version: 0.1
#################################################################################################
# ChangeLog
# 0.1: 5Jan21: Initial Release
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
curl -k -v -XDELETE -H "Authorization: Bearer $APPToken" -F server='*' https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/ipfilter/param/${BlockFeed}

sleep 10

echo "- Updating feed contents in ATP Cloud..."
curl -k -v -XPOST -H "Authorization: Bearer $APPToken" -F file=@${blockList} https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/ipfilter/file/${BlockFeed}

sleep 2
# Clean up temporary file
rm $blockList

echo "-- COMPLETE: Feed Successfully Update!!"
sleep 5

## End of script #
