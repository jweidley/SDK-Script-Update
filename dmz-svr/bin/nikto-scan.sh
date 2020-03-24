#!/bin/bash
# Purpose: Run contstant Nikto scans to generate IPS alerts on vSRX
# Version: 0.1
#######################################################################

################
# Variables
################
NIKTO="/usr/bin/nikto"
TARGET="192.168.100.20"
SLEEP="/bin/sleep"

################
# Main
################
while true; do
	for levels in 7 7 8 7 7 x; do
		echo "======================================================"
		echo "============= Running scan at level: $levels"
		echo "======================================================"
		$NIKTO -host $TARGET -Tuning $levels
		echo "================= Sleeping...."
		$SLEEP 60
	done
done

## End of script ##
