#!/bin/bash
# Purpose: Update SDK scripts
# Version: 0.7
#############################################################
# ChangeLog:
# 0.1: Initial Release
# 0.2: 24Mar20: Public Release
# 0.3: 13Apr20: Added version tracking (.sdk-script-version)
# 0.4: 14Apr20: Added logic to only upgrade if needed based on script version
# 0.5: 17Dec20: Added condition for lubuntu-20
# 0.6: 7Jan21: Added condition for ubuntu-20
# 0.7: 21Feb21:  version 20 specific, fixed backup issue on clean installs
#############################################################

####################
# Variables
####################
HOSTNAME=`/bin/hostname`
BASE_DIR="/usr/local/bin"
BACKUP_DIR="/usr/local/bin/SCRIPT-BACKUP"
CONFIG_DIR="/etc/sdk"

####################
# Functions
####################
performUpgrade () {
    echo "- Setting script source directory to $SCRIPT_DIR"

    ########################
    # BACKUP
    ########################
    # Check for other script backups and remove them
    if [ -d $BACKUP_DIR ]; then
        echo "- Removing old script backups"
        sudo rm -rf $BACKUP_DIR
        echo "- Making Script Backup Directory: $BACKUP_DIR"
        sudo mkdir $BACKUP_DIR
        echo "- Backuping up existing scripts"
        sudo cp ${BASE_DIR}/demo-menu $BACKUP_DIR
        sudo cp ${BASE_DIR}/*.py $BACKUP_DIR
        sudo cp ${BASE_DIR}/*.sh $BACKUP_DIR
    else
        echo "- NO old script backups found"
        echo "- Making Script Backup Directory: $BACKUP_DIR"
        sudo mkdir $BACKUP_DIR
    fi

    # Make a backup of the sdk.conf
    if [ -d $CONFIG_DIR ]; then
        echo "- Creating backup copy of sdk.conf"
        sudo cp ${CONFIG_DIR}/sdk.conf ${CONFIG_DIR}/sdk.conf.bak
    else
        echo "- Creating config directory ${CONFIG_DIR}"
        sudo mkdir ${CONFIG_DIR}
    fi

    # Backup Lubuntu scripts
    if [[ $HOSTNAME == "lubuntu" ]]; then
    	echo "  + Backuping up lubuntu scripts directory"
    	sudo cp -R /home/juniper/Scripts/* $BACKUP_DIR
    fi

    ########################
    # INSTALL
    ########################
    # Copy conf file to CONFIG_DIR
    echo "- Copying new sdk.conf to ${CONFIG_DIR}"
    sudo cp ${ETC_DIR}/sdk.conf ${CONFIG_DIR}

    # Copy new scripts to SCRIPT_DIR
    echo "- Copying new scripts to $BASE_DIR"
    sudo cp ${SCRIPT_DIR}/bin/* $BASE_DIR
    sudo cp ${VERSION} ${BASE_DIR}

    # Copy new Lubuntu scripts
    if [[ $HOSTNAME == "lubuntu" ]]; then
    	echo "  + Copying new lubuntu scripts"
    	sudo cp -R ${SCRIPT_DIR}/scripts/* /home/juniper/Scripts/
    fi

    echo "- Setting permissions and ownership of new script files"
    sudo chmod 755 ${BASE_DIR}/*
    sudo chown root:root ${BASE_DIR}/*

   	# Lubuntu specific
    if [[ $HOSTNAME == "lubuntu" ]]; then
   		echo "  + Setting permissions on new Lubuntu scripts"
   		sudo chmod 755 /home/juniper/Scripts/*
   		sudo chown juniper:juniper /home/juniper/Scripts/*
   	fi

   	# Clean up install directory
   	# admin-menu
   	if [ -d /tmp/SDK-Script-Update ]; then
   		echo "- Removing downloaded file"
   		sudo rm -rf /tmp/SDK-Script-Update
   	else
   		echo "!! Ensure you manually remove the download directory: $PWD !! "
   	fi

   	## End
   	echo "---------- Finished ----------"
   	echo " "
}


####################
# Main
####################
# Find hostname to determine which scripts to update.
if [[ $HOSTNAME == "dmz-svr" ]]; then
    # Check /tmp for admin-menu
    if [ -d /tmp/SDK-Script-Update ]; then
        VERSION="/tmp/SDK-Script-Update/.sdk-script-version"
    	SCRIPT_DIR="/tmp/SDK-Script-Update/dmz-svr20"
    	ETC_DIR="/tmp/SDK-Script-Update/dmz-svr20/etc"
    # Default to the current directory for manual
    else
        PWD=`/bin/pwd`
    	VERSION="${PWD}/.sdk-script-version"
    	SCRIPT_DIR="${PWD}/dmz-svr20"
        ETC_DIR="${PWD}/dmz-svr20/etc"
   	fi
elif [[ $HOSTNAME == "lubuntu" ]]; then
    # Check /tmp for admin-menu
   	if [ -d /tmp/SDK-Script-Update ]; then
   		VERSION="/tmp/SDK-Script-Update/.sdk-script-version"
   		SCRIPT_DIR="/tmp/SDK-Script-Update/lubuntu20"
   		ETC_DIR="/tmp/SDK-Script-Update/lubuntu20/etc"
   	# Default to the current directory for manual
   	else
        PWD=`/bin/pwd`
        VERSION="${PWD}/.sdk-script-version"
    	SCRIPT_DIR="${PWD}/lubuntu20"
    	ETC_DIR="${PWD}/lubuntu20/etc"
    fi
else
    echo "!! ERROR !! - No valid server type found."
   	exit
fi

# Version Check
newVer=`cat ${VERSION} | grep Version | awk '{print $3}' | sed 's/v//'`
echo "- Checking script versions..."

# Condition for VMs with script update feature enabled
if [ -f /usr/local/bin/.sdk-script-version ]; then
    currentVer=`cat /usr/local/bin/.sdk-script-version | grep Version | awk '{print $3}' | sed 's/v//'`

    if (( $(echo "$newVer  $currentVer" | awk '{print ($1 <= $2)}') )); then
        echo "  + NO upgrade necessary: Current version: ${currentVer}, New Version: ${newVer}"
        exit
    else
        echo "  + Upgrade Required: Current version: ${currentVer}, New Version: ${newVer}"   
        performUpgrade
        
    fi
# Condition to catch old VMs prior to script update feature
else
    echo "  + Upgrade Required: Current version: NA, New Version: ${newVer}"   
    performUpgrade

fi

## End of Script ##
