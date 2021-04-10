#!/bin/bash
# Purpose: Add/Remove Command & Control URL Threat Feed in ATP Cloud
#	   URL list.
# Author: John Weidley (Sample code provided by Craig Dods, Michael Bergt)
# Version: 0.1
#################################################################################################
# ChangeLog
# 0.1: 10Mar21: Initial Release
#################################################################################################

##########################
# Variables
##########################
# API Token that was generated in the ATP cloud WebUI (Administration > Application Tokens)
# The token from ATP Cloud should be inside the double quotes in 1 continuous line.
#APPToken="ADD-YOUR-TOKEN-HERE"
APPToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Imp3ZWlkbGV5QGp1bmlwZXIubmV0IiwidG9rZW5faWQiOiJmOTBiOWRhYy0xYzEzLTQyMmUtYmVhYi0yYWRjNDVkZWQyNTQiLCJ0b2tlbl9uYW1lIjoiUmVjb21tZW5kZWRfSVBfQmxvY2siLCJhY2Nlc3NfZ3JvdXBzIjpbIk9wZW4gQVBJIl0sImV4cCI6MTYzNzg0MTExMSwiZ2VuaWQiOiJMNFhpdnduNGp6eTBWd0htOGlWaTRLZTREMFZybFQxVVEyaGNyak5qV0ZnWDF6cndSZ1lyQ0xreVdNeEFWYmloNWF5OG5DV252TE95Skx6SEpMVUl2OGVjTFlQcnVwaWVKd0FXaWdpb0pCZz0ifQ.awf1jdpwNL4YlVmwQtthAqVcJzxz3Li8VCS-G5y89eU"

# CC Feed name to be create in ATP Cloud
BlockFeed="URL_Blocks"

# Dynamic tmp file 
blockList="/tmp/urlblockList.txt"

# Populate the blocklist with the following content. format: URL,Threat-level
fileContents=(
	"https://putty.org,9"
	"https://winmerge.org,10"
	"https://winscp.net,9"
	"https://www.cisco.com,9"
	"https://www.makeuseof.com/category/mac,9"
	"https://www.makeuseof.com/category/windows,9"
	)


################################################################
# buildBlockList: Create tmp file with fileContents list
################################################################
buildBlockList() {
	# Sanity Check
	if [ -f "$blockList" ]; then
		echo "   + Cleaning up existing block list..."
		sudo rm $blockList
	fi

	# Build BlockList
	for line in ${fileContents[*]}
	do
		echo $line >> $blockList
	done
}

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
			"https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/cc/param/url/${BlockFeed}"
			) || code="$?"
	elif [ $1 == "add" ]; then
		statuscode=$(curl -s -k -w "%{http_code}" -XPOST -H "Authorization: Bearer $APPToken" -F file=@${blockList} \
			-o >(cat >/tmp/curl_body) \
			"https://threat-api.sky.junipersecurity.net/v2/cloudfeeds/cc/file/url/${BlockFeed}"
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
		echo "   + Message: $body"
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
echo " ATP API: URL Feed Demo"
echo "========================================================================"

# Sanity check APPToken variable
if [ $APPToken == "ADD-YOUR-TOKEN-HERE" ]; then
	echo "ERROR: The APPToken variable hasn't been set!"
	echo "  - Go to ATP Cloud WebUI (Administration > Application Tokens) to generate one"
	echo "  - Add Token to /usr/local/bin/atp-api-ipfilter.sh script"
	sleep 10
	exit
fi

echo "- Deleting feed contents from ATP Cloud..."
curlWithStatus delete
sleep 10

echo "- Generating Feed file..."
buildBlockList

echo "- Updating feed contents in ATP Cloud..."
curlWithStatus add
sleep 2

# Clean up temporary file
rm $blockList

echo "-- COMPLETE: Feed Successfully Update!!"

## End of script #
