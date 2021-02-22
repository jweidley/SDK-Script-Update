#!/usr/bin/python3
# Purpose: DMZ-Svr Extras Menu. Used to easily run undocumented scripts/demos
# Author: John Weidley
# Version: 0.1
######################################################################################
# ChangeLog
# 0.1: 5Jan21: Initial Release
######################################################################################

################
# Modules
################
from os import system
from time import sleep

################
# Functions
################
def main():
	choice = '0'
	while choice == '0':
		system("/usr/bin/clear")
		print("=======================================================================")
		print("|| Juniper SRX Demo Kit: Extras Menu                                 ||")
		print("=======================================================================")
		print("1) ATP Cloud: API: IPFilter")
		print("2) ATP Cloud: Adaptive Threat Profiling")
		print("\nq) Quit the menu")
		print("=======================================================================")
		choice = input("\nPlease select a menu item: ")

		if choice == "1":
			system("/usr/bin/clear")
			print("....Running Scan...")
			sleep(3)
			system("/usr/local/bin/atp-api-ipfilter.sh")
			main()
		elif choice == "2":
			system("/usr/bin/clear")
			print("....Running Adaptive Threat Profiling Traffic...")
			sleep(3)
			system("/usr/local/bin/atp-AdaptThreatProf.py")
			main()
		elif choice == "q":
			print("Exiting...")
			exit()
		else:
			print("Invalid option...")
			sleep(2)
			system("/usr/bin/clear")
			main()

main()

## End of Script ##
