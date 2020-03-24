#!/usr/bin/python3
# Purpose: Open the web browser and tabs with the URLs below to demo UTM Webfiltering.
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

webbrowser.open('https://www.glassdoor.com')
sleep(5)
webbrowser.open('https://www.monster.com')
sleep(3)
webbrowser.open('https://www.juniper.net')
sleep(3)


## End of Script ##

