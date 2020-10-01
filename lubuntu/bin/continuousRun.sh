#!/bin/bash
# Purpose: Run continuous downloads/scans
# Version: 0.5
# Author: John Weidley
#####################################################################################################
# 0.1: 6Apr20: Intial Release
# 0.2: 9Apr20: Launch in separate windows
# 0.3: 17Apr20: Added AppTrack generation
# 0.4: 8May20: Added gnome-terminal condition
# 0.5: 22Sep20: Added UserFW User Switcher
#####################################################################################################

######################
# Variables
######################
PYTHON="/usr/bin/python3"
EXT_DOWNLOAD="/usr/local/bin/bad-extension-download.py --continuous"
VIRUS_DOWNLOAD="/usr/local/bin/virus-download.py --continuous"
PS_OUTPUT=`ps -ef | egrep '\-\-continuous'`

######################
# Main
######################
# Main Banner
echo "######################################################################"
echo " Continuous Traffic:"
echo "######################################################################"

# Check command line arguments
if [ $# -ne 1 ]; then
	echo "ERROR: Missing argument!"
	echo "Usage: $0 [start|stop]"
	exit
fi

# Process arguments & take action
case $1 in
	start)
		if [[ $PS_OUTPUT ]]; then
			echo " "
			echo "!!!!...Continus Scan Already in Progress....no action"
			echo " "
			sleep 5
			exit
		else
			echo "- Opening Traffic Generating Website"
			/usr/bin/firefox --new-tab http://www.emojitracker.com/ 2>/dev/null&
			sleep 3
			echo "- Opening Traffic Generating Website"
			/usr/bin/firefox --new-tab "https://trends.google.com/trends/hottrends/visualize?nrow=5&ncol=5" 2>/dev/null&
			sleep 3
			if [ -f /usr/bin/gnome-terminal1 ]; then
			echo "- Starting Traffic Generators..."
			gnome-terminal --tab -t "SwitchUser" --command "/usr/local/bin/userFW_switchUser.py --continuous" \
                --tab -t "AppTrack" --command "/usr/local/bin/apptrack-generate.py --continuous" \
				--tab -t "Virus" --command "/usr/local/bin/virus-download.py --continuous" \
				--tab -t "Content-Filter" --command "/usr/local/bin/bad-extension-download.py --continuous" \
				--tab -t "EnhancedWebFilter" --command "/usr/local/bin/webfilter-download.py --continuous" \
				--tab -t "WebTraffic" --command "/usr/local/bin/webTrafficGen.py --continuous"
			else
			echo "- Running UserFW Switcher..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/userFW_switchUser.py --continuous" 2>/dev/null &
			echo "- Running AppTrack Traffic..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/apptrack-generate.py --continuous" 2>/dev/null &
			echo "- Running download of test virii..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/virus-download.py --continuous" 2>/dev/null &
			echo "- Running download of bad extensions..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/bad-extension-download.py --continuous" 2> /dev/null &
			echo "- Running Blocked Web Traffic..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/webfilter-download.py --continuous" 2>/dev/null &
			echo "- Running Permitted Web Traffic..."
			/usr/bin/lxterminal --geometry=75x12 --command="/usr/local/bin/webTrafficGen.py" 2>/dev/null &
			fi
			echo " "
			echo "-- Finished --"
			echo " "
			exit
		fi
		;;

	stop)	echo " "
		if [[ $PS_OUTPUT ]]; then
			echo " "
			echo "-Killing continuous downloads...."
			sudo kill -9 `ps -ef | egrep '\-\-continuous' | egrep -v egrep | awk '{print $2}'`
			sudo kill -9 `ps -ef | egrep 'webTraffic' | egrep -v grep | awk '{print $2}'`
			echo " "
			echo "-- Finished --"
			exit
		else
			echo "!!....No processes to kill"
			echo " "
			echo "-- Finished --"
			exit
		fi
		sleep 5
		;;

	*)	echo "ERROR: Missing argument!"
		echo "Usage: $0 [start|stop]"
		exit
		;;
esac

## End of Script ##
