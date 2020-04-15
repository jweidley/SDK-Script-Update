#!/bin/bash
# Purpose: Run continuous scans
# Version: 0.2
# Author: John Weidley
##################################################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 14Apr20: Progress bar moved to function for flexibility
##################################################################################

######################
# Variables
######################
PYTHON="/usr/bin/python3"
SCREEN_SCAN="/usr/local/bin/hping3-scan.py --continuous"
IPS_SCAN="/usr/local/bin/nikto-scan.py --continuous"
PS_OUTPUT=`ps -ef | egrep '\-\-continuous'`

######################
# Functions
######################
progressBar () {
	clear
	echo "######################################################"
	echo " Continuous Traffic"
	echo "  - SCREENS"
	echo "  - IDP"
	echo " (press ctrl+c to return to menu)"
	echo "######################################################"
	echo " "
	while true
	do
		echo -ne 'In Progress:[                                      ]\r'
		sleep .5
		echo -ne 'In Progress:[===                                   ]\r'
		sleep .5
		echo -ne 'In Progress:[========                              ]\r'
		sleep .5
		echo -ne 'In Progress:[=============                         ]\r'
		sleep .5
		echo -ne 'In Progress:[====================                  ]\r'
		sleep .5
		echo -ne 'In Progress:[=============================         ]\r'
		sleep .5
		echo -ne 'In Progress:[======================================]\r'
		sleep .5
	done
}


######################
# Main
######################
# Main Banner
echo "######################################################"
echo " Continuous Traffic:"
echo "######################################################"

# Check command line arguments
if [ $# -ne 1 ];then
	echo "ERROR: Missing argument!"
	echo "Usage: $0 [start|stop]"
	exit
fi

# Process arguments & take action
case $1 in
	start) 
		if [[ $PS_OUTPUT ]]; then
			progressBar
		else
			$PYTHON $SCREEN_SCAN 1> /dev/null 2>&1 &
			$PYTHON $IPS_SCAN 1> /dev/null 2>&1 &

			# Start process bar
			progressBar
		fi
		;;

	stop) 	
		echo "- Killing processes...."
		echo " "
		sudo kill -9 `ps -ef | egrep '\-\-continuous' | egrep -v egrep | awk '{print $2}'`
		sleep 5
		;;

	*)	echo "ERROR: Missing argument!"
		echo "Usage: $0 [start|stop]"
		exit
		;;
esac

## End of Script ##
