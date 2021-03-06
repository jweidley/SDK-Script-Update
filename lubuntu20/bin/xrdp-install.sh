#!/bin/bash
# Purpose: Install XRDP for Lubuntu 
# Version: 0.1
# Author: John Weidley
# Reference: http://c-nergy.be/blog/?p=6692
##############################################################################
# ChangeLog
# 0.1: 5Mar21: Initial Release
##############################################################################
#
# CURRENT STATUS OF THIS SCRIPT....
# Only created the VERSION variable. Trying to figure out how to handle the
# different versions. The 18.04 'here' document could be problems???
#
##############################################################################

# Variables
HOSTNAME=`/bin/hostname`
VERSION=`egrep 'VERSION_ID' /etc/os-release | awk -F= '{print $2}' | sed s/\"//g`

# functions
installXRDP () {
    echo " - Updating repos..."
    sudo apt-get update
    echo " "
    echo "-------------------------------------------------------------------"
    echo " - Installing XRDP and dependencies..."
    sudo apt install -y xrdp

    echo " "
    echo "-------------------------------------------------------------------"
    echo " - Tweaking cursor configuration..."
    sudo sed -e 's/^new_cursors=true/new_cursors=false/g' -i /etc/xrdp/xrdp.ini

    echo " "
    echo "-------------------------------------------------------------------"
    echo " - Restarting XRDP service..."
    sudo systemctl enable xrdp
    sudo systemctl restart xrdp

    echo " "
    echo "-------------------------------------------------------------------"
    echo " - Creating xsession files for users..."
    echo "startlxqt" > /tmp/xrdp-xsession
    echo "   + juniper user..."
    sudo cp /tmp/xrdp-xsession /home/juniper/.xsession
    sudo chown juniper:juniper /home/juniper/.xsession
    echo "   + demo-user user..."
    sudo cp /tmp/xrdp-xsession /home/demo-user/.xsession
    sudo chown demo-user:demo-user /home/demo-user/.xsession
    sudo rm /tmp/xrdp-xsession

}
# Main
echo "========================================================================"
echo "  Installing XRDP on Lubuntu"
echo "========================================================================"

# Sanity Check for Lubuntu 20.04
if [[ $HOSTNAME == "lubuntu" && $VERSION == "20.04" ]]; then
    installXRDP
else
    echo "!!!! Invalid host. Quitting. !!!!"
    exit
fi

echo " "
echo " "
echo " "
echo " ------------ XRDP Installation Completed ------------"
echo "     - Reboot system then test RDP"

## End of Script ##
