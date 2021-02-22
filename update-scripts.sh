#/bin/bash
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

####################
# Main
####################
echo "========================================================"
echo " SDK Script Update"
echo "========================================================"
if [[ $OSVERSION == "18.04" ]]; then
    echo "- Found version 18..."
    update18.sh
elif [[ $OSVERSION == "20.04" ]]; then
    echo "- Found version 20..."
    update20.sh
else
    echo "!! No supportable versions found...exiting !!"
    exit
fi

## End of Script ##
