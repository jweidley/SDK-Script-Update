#!/bin/bash
# Purpose: Run continuous scans
# Version: 0.1
# Author: John Weidley
##################################################################################

######################
# Variables
######################
PYTHON="/usr/bin/python3"
SCREEN_SCAN="/usr/local/bin/hping3-scan.py --continuous"
IPS_SCAN="/usr/local/bin/nikto-scan.py --continuous"
PS_OUTPUT=`ps -ef | egrep '\-\-continuous'`

######################
# Main
######################
# Main Banner
echo "#########################################################################"
echo " Continuous Traffic:"
echo "#########################################################################"

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
			echo " "
			echo "!!!!...Continuous Scan Already in Progress....no action"
			echo " "
			sleep 5
			exit
		else
			# Start Progress bar
			$PYTHON $SCREEN_SCAN 1> /dev/null 2>&1 &
			$PYTHON $IPS_SCAN 1> /dev/null 2>&1 &
			clear
			echo "######################################################"
			echo " Continuous Traffic"
			echo "  - SCREENS"
			echo "  - IDP"
			echo " (press ctrl+c to return to menu)"
			echo "######################################################"
			echo " "

			# Start process loop
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
		fi
		;;

	stop) 	
		echo "- Killing continuous scans...."
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
