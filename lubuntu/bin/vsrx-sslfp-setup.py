#!/usr/bin/python3
# Purpose: vSRX SSL Forward Proxy setup on vSRX. 
# Version: 0.1
#
############################################################################################################
# CHANGELOG:
# - 0.1: Initial Release
############################################################################################################
# NOTES:
############################################################################################################

################
# Modules
################
import sys
from lxml import etree
from os import system
import re
from getpass import getuser
from time import sleep
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import RpcTimeoutError
import requests
from paramiko import SSHClient
from scp import SCPClient

################
# Variables
################
class style:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

filename = "cacert.pem"
url = "https://curl.haxx.se/ca/" + filename
caFile = ""

# Firewall Variables
user = "juniper"
passwd = "juniper123"
vsrx = "192.168.100.1"
dev = Device(host=vsrx,gather_facts='False',user=user,password=passwd)

# CA Cert Variables
caGroupName = "ssl-ca-bundle"
cert_id = "SSL-FP-CERT"
size = "2048"
type = "rsa"
domain_name = "sec-demo.net"
subject = "CN=SSL_PROXY"
email = "admin@sec-demo.net"
etype = "pem"
export_name = "sdk-sslproxy-root.crt"
export_file = "/var/tmp/" + export_name

################
# Functions
################
def configureFFP(dev):
    print(style.BOLD + "- Creating Key Pair: type: " + type + " Size: " + size + style.END)
    cmd1 = dev.rpc.generate_pki_key_pair(certificate_id=cert_id, \
                                            size=size, \
                                            type=type)
    print(etree.tostring(cmd1,pretty_print=True,encoding='unicode'))
    print
    sleep(3)

    print(style.BOLD + "- Creating CA Certificate" + style.END)
    cmd2 = dev.rpc.generate_pki_self_signed_local_certificate(certificate_id=cert_id, \
                                                                domain_name=domain_name, \
                                                                subject=subject, \
                                                                email=email, \
                                                                add_ca_constraint=True)
    print(etree.tostring(cmd2,pretty_print=True,encoding='unicode'))
    print
    sleep(3)

    print(style.BOLD + "- Exporting CA Certificate" + style.END)
    cmd3 = dev.rpc.request_security_local_certificate_export(certificate_id=cert_id, \
                                                                type=etype, \
                                                                filename=export_file)
    print(etree.tostring(cmd3,pretty_print=True,encoding='unicode'))
    print
    sleep(3)

def loadCaGroup(dev):
    print(style.BOLD + "- Importing CA bundle...(this will take a few minutes)" + style.END)

    try:
        cmd3 = dev.rpc.request_security_pki_ca_profile_group_load(ca_group_name=caGroupName,filename=filename)
        print("  + CA Bundle successfully loaded")
        #print(etree.tostring(cmd3,pretty_print=True,encoding='unicode'))
        print
        sleep(3)
    except RpcTimeoutError as err:
        print("\tA timeout has occurred: {0}".format(err))
        print
        exit()

    sleep(3)

################
# Main
################
print(style.BOLD + "=================================================================" + style.END)
print(style.BOLD + "   SRX: SSL Forward Proxy Setup  " + style.END)
print(style.YELLOW + "  - Ensure the BASE config is loaded on the vSRX!" + style.END)
print(style.BOLD + "=================================================================" + style.END)

######################################
# Download CA bundle from Internet
######################################
try:
    print(style.BOLD + "- Downloading Cert bundle..." + style.END)
    caFile = requests.get(url)
except requests.exceptions.ConnectionError as err:
    print("\tCannot connect to device: {0}".format(err))
    print
    print("---------------------------------------------------------")
    print("!! File download failed: Check Internet connectitvity. !!")
    print
    exit()

if caFile:
    print(style.BOLD + "- Writing CA Cert file locally" + style.END)
    open(filename, 'wb').write(caFile.content)
else:
    print("!! Failed to write file. Check permissions of the current directory. !!")
    exit()


######################################
# Upload CA bundle to vSRX
######################################
ssh = SSHClient()
ssh.load_system_host_keys()

try:
    ssh.connect(hostname=vsrx,username=user,password=passwd)
except Exception as err:
    print("\tCannot connect to device: {0}".format(err))
    print("!! Failed to connect to the vSRX. Check connectivity. !!")
    exit()

if ssh.connect:
    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    print(style.BOLD + "- Transferring CA Cert file to vSRX..." + style.END)
    scp.put(filename)
else:
    print("!! No active ssh connection. Exiting!!")


######################################
# Configure SSL Proxy on vSRX
######################################
# Make connection to the vSRX and check to see if the cert already exists
try:
    dev.open()
    dev.timeout = 300
    look = dev.rpc.get_pki_local_certificate(certificate_id=cert_id)

except ConnectError as err:
	print("!!..The vSRX appears to be down..!!")
	print("Cannot connect to device: {0}".format(err))
	sleep(3)
	sys.exit(1)

except Exception as err:
	print("!!..The vSRX appears to be down..!!")
	print(err)
	sleep(3)
	sys.exit(1)

# Figure out what to do
if len(look):
    print("!! SSL Forward Proxy has already been configured. Exiting..!")
    exit
else:
    configureFFP(dev)

######################################
# Copy exported vSRX root CA to local
######################################
print(style.BOLD + "- Transferring CA Cert file to vSRX..." + style.END)
scp.get(export_file, export_name)

######################################
# Load CA Bundle on vSRX
######################################
loadCaGroup(dev)

######################################
# Load SSL Proxy cert locally
# - This is required for script updates (and other functions)
######################################
print(style.BOLD + "- Copying SSL Proxy Cert to OS Store..." + style.END)
system("sudo cp " + export_name + " /usr/local/share/ca-certificates")
sleep(3)

print(style.BOLD + "- Rebuilding OS Certificate Store..." + style.END)
system("sudo update-ca-certificates")
sleep(3)

######################################
# Clean up
######################################
dev.close()                 ## Close Netconf session
scp.close()                 ## Close secure copy session
system("rm " + filename)    ## Remove cert bundle

print
print("-------------------------------------------------------------------------------------")
print(" SSL Forward Proxy Configuration is complete! --")
print
print(" -- NEXT STEPS:") 
print(" Lubuntu:")
print("  1. The vSRX CA cert (sdk-sslproxy-root.crt) is in the current directory. Add this file")
print("     to the browsers certificate store & restart the browser before testing.")
print
print(" vSRX:")
print("  1. Load the partial SSLFP configuration (PARTIAL-SDK-vsrx1-SSLFP.conf)")
print
print("-------------------------------------------------------------------------------------")
print

## End of Script ##
