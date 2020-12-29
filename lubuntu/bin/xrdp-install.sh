#!/bin/bash
# Purpose: Install XRDP for Lubuntu 18.04
# Version: 0.1
# Author: John Weidley
# Reference: https://www.hiroom2.com/2018/05/07/ubuntu-1804-xrdp-lxde-en/
##############################################################################
# ChangeLog
# 0.1: 28Dec20: Initial Release
##############################################################################

# Variables
HOSTNAME=`/bin/hostname`

# Main
echo "========================================================================"
echo "  Installing XRDP on Lubuntu"
echo "========================================================================"

# Sanity Check for Lubuntu 18.04
if [[ $HOSTNAME != "lubuntu-wks" ]]; then
    echo "!!!! Invalid host. Quitting. !!!!"
    exit
fi

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
echo "lxsession -s Lubuntu -e LXDE" > /tmp/xrdp-xsession
echo "   + juniper user..."
sudo cp /tmp/xrdp-xsession /home/juniper/.xsession
sudo chown juniper:juniper /home/juniper/.xsession
echo "   + demo-user user..."
sudo cp /tmp/xrdp-xsession /home/demo-user/.xsession
sudo chown demo-user:demo-user /home/demo-user/.xsession
sudo rm /tmp/xrdp-xsession

echo " "
echo "-------------------------------------------------------------------"
echo " - Creating Wrapper..."
sleep 5
sudo cp /usr/bin/light-locker /usr/bin/light-locker.orig
sleep 5
cat <<'EOF' >> /tmp/light-locker
#!/bin/sh

# The light-locker uses XDG_SESSION_PATH provided by lightdm.
if [ ! -z "\${XDG_SESSION_PATH}" ]; then
  /usr/bin/light-locker.orig
else
  # Disable light-locker in XRDP.
  true
fi
EOF

sleep 5
sudo rm /usr/bin/light-locker
sudo cp /tmp/light-locker /usr/bin/light-locker
sudo chmod a+x /usr/bin/light-locker

echo " "
echo " "
echo " "
echo " ------------ XRDP Installation Completed ------------"
echo "     - Reboot system then test RDP"

## End of Script ##
