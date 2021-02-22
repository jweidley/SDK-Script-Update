#!/bin/csh
# Purpose: Convert SDK configs for management via untrust interface (instead of fxp0)
# Version: 0.2
# Author: John Weidley
#---------------------------------------------------------------------------
# HOWTO:
# 1. On the vSRX, put this script in the same directory with the SDK configuration files
# 2. Enter the shell on the vSRX
# 3. Edit the untrustIP & gateway variables to suit your environment and save
# 4. Run the script by typing '/bin/csh ./convertConfigs4UntrustMgmt.sh'
#
# ! The .txt files will be modified by the script and the original configs
#   are saved with a .orig extension.
############################################################################
 
############################################################################
################# SET YOUR VARIABLES #######################################
############################################################################
# Set untrust interface IP address/mask (ge-0/0/0)
set untrustIP="192.168.5.153/24"
 
# Set the default gateway IP address for your environment
set gateway="192.168.5.1"
 
# Set IP address of Space/Log Collector
set lcIP="192.168.3.13"
 
# Should the script add the Log Collect configs? (1=yes, 0=no)
set addLC=1
 
############################################################################
################# NO CHANGES BEYOND THIS POINT #############################
############################################################################
echo "=========================================================="
echo " SDK: Converting Demo Configs for Untrust Mgmt"
echo "=========================================================="
 
foreach file (`ls *SDK*.conf`)
        echo "Converting $file ..."     
 
        # Substitute fxp0 lines with ge-0/0/0
        sed -i .orig -e \
        's@set interfaces ge-0/0/0 description "untrust;Internet-via-NAT"@set interfaces ge-0/0/0 description "untrust;Internet"@' -e \
        "s@set interfaces ge-0/0/0 unit 0 family inet dhcp@set interfaces ge-0/0/0 unit 0 family inet address $untrustIP@" -e \
        's/set interfaces fxp0 description "Laptop:Private Bridge"/set interfaces fxp0 description DISABLED/' -e \
        's/set interfaces fxp0 unit 0 family inet dhcp/set interfaces fxp0 disable/' -e \
        's@set system services web-management http interface fxp0.0@set system services web-management http interface ge-0/0/0.0@' $file
 
        # Add Default route
        echo "set routing-options static route 0.0.0.0/0 next-hop $gateway" >> $file
 
        # Add Log Collector configuration lines
        if ($addLC == 1) then
                echo "  + Adding Log Collector CLIs to configs ..."
                echo "set security log stream LOG-COLLECTOR severity info" >> $file
                echo "set security log stream LOG-COLLECTOR format sd-syslog" >> $file
                echo "set security log stream LOG-COLLECTOR category all" >> $file
                echo "set security log stream LOG-COLLECTOR host $lcIP" >> $file
                echo "set security log stream LOG-COLLECTOR host port 514" >> $file
        endif
end
echo " "
echo "--Finished--"
 
## end of script ##
