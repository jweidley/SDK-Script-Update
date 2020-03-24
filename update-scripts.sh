#!/bin/bash
# Purpose: Update SDK scripts
# Version: 0.2
#############################################################

####################
# Variables
####################
HOSTNAME=`/bin/hostname`
BASE_DIR="/usr/local/bin"
BACKUP_DIR="/usr/local/bin/SCRIPT-BACKUP"

####################
# Main
####################
# Start Banner
echo "========================================================"
echo " SDK Script Update"
echo "========================================================"

# Find hostname to determine which scripts to update.
if [[ $HOSTNAME == "SDK-dmz-svr" ]]; then
	# Check for /tmp for admin-menu
	if [ -d /tmp/SDK-Script-Update ]; then
		SCRIPT_DIR="/tmp/SDK-Script-Update/dmz-svr"
	# Default to the current directory
	else
        	PWD=`/bin/pwd`
		SCRIPT_DIR="${PWD}/dmz-svr"
	fi
elif [[ $HOSTNAME == "lubuntu-wks" ]]; then
	# Check for /tmp for admin-menu
	if [ -d /tmp/SDK-Script-Update ]; then
		SCRIPT_DIR="/tmp/SDK-Script-Update/lubuntu"
	# Default to the current directory
	else
        	PWD=`/bin/pwd`
		SCRIPT_DIR="${PWD}/lubuntu"
	fi
else
        echo "!! ERROR !! - No valid server type found."
	exit
fi
echo "- Setting script source directory to $SCRIPT_DIR"

# Check for other script backups and remove them
if [ -d $BACKUP_DIR ]; then
	echo "- Removing old script backups"
	sudo rm -rf $BACKUP_DIR
else
	echo "- NO old script backups found"
fi

# Backup existing scripts
echo "- Making Script Backup Directory: $BACKUP_DIR"
sudo mkdir $BACKUP_DIR

echo "- Backuping up existing scripts"
sudo cp ${BASE_DIR}/demo-menu $BACKUP_DIR
sudo cp ${BASE_DIR}/*.py $BACKUP_DIR
sudo cp ${BASE_DIR}/*.sh $BACKUP_DIR

# Backup Lubuntu scripts
if [[ $HOSTNAME == "lubuntu-wks" ]]; then
	echo "  + Backuping up lubuntu scripts directory"
	sudo cp -R /home/juniper/Scripts/* $BACKUP_DIR
fi

# Copy new scripts to SCRIPT_DIR
echo "- Copying new scripts to $BASE_DIR"
sudo cp ${SCRIPT_DIR}/bin/* $BASE_DIR

# Copy new Lubuntu scripts
if [[ $HOSTNAME == "lubuntu-wks" ]]; then
	echo "  + Copying new lubuntu scripts"
	sudo cp -R ${SCRIPT_DIR}/scripts/* /home/juniper/Scripts/
fi

echo "- Setting permissions and ownership of new script files"
sudo chmod 755 ${BASE_DIR}/*
sudo chown root:root ${BASE_DIR}/*

# Lubuntu specific
if [[ $HOSTNAME == "lubuntu-wks" ]]; then
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

## End of Script ##
