#!/bin/bash
# Purpose: Wrapper to call the correct update script.
# Version: 0.1
#############################################################
# ChangeLog:
# 0.1: Initial Release
#############################################################

####################
# Variables
####################
OSVERSION=`egrep VERSION_ID /etc/os-release | awk -F= '{print $2}' | sed s/\"//g`

# Update via the admin menu
if [ -d /tmp/SDK-Script-Update ]; then
    SCRIPT_DIR="/tmp/SDK-Script-Update"
# Default to the current directory for manual
else
    PWD=`/bin/pwd`
    SCRIPT_DIR="${PWD}"
fi

####################
# Main
####################
echo "========================================================"
echo " SDK Script Update"
echo "========================================================"
if [[ $OSVERSION == "18.04" || $OSVERSION == "16.04" ]]; then
    echo "- Original version found..."
    $SCRIPT_DIR/update18.sh
elif [[ $OSVERSION == "20.04" ]]; then
    echo "- Found version 20..."
    $SCRIPT_DIR/update20.sh
else
    echo "!! No supportable versions found...exiting !!"
    exit
fi

## End of Script ##
