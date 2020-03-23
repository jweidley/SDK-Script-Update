#!/usr/bin/python3
# Purpose: Open the web browser and tabs with the URLs below to demo UTM blacklisting.
# Version: 0.1
#########################################################################################

################
# Modules
################
import webbrowser
from time import time,sleep

################
# Main
################
print("======================================")
print(" ... Opening web pages ...")
print("======================================")

webbrowser.open('https://www.cisco.com')
sleep(5)
webbrowser.open('http://developer.cisco.com')
sleep(3)
webbrowser.open('http://community.cisco.com')
sleep(3)


## End of Script ##

