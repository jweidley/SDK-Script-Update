#!/usr/bin/python3
# Purpose: DMZ-Svr Menu
# Version: 0.2
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
		print("|| Juniper SRX Demo Kit: DMZ-SVR Menu                                ||")
		print("=======================================================================")
		print("1) Screen Demo: Run Scan to Trusted Network")
		print("2) IPS Demo: Run Web Scan to Metasploitable")
		print("\nq) Quit the menu")
		print("=======================================================================")
		choice = input("\nPlease select a menu item: ")

		if choice == "1":
			system("/usr/bin/clear")
			print("....Running Scan to Trust Network to generate Screen alarms...")
			sleep(3)
			system("/usr/local/bin/hping3-scan.py")
			main()
		if choice == "2":
			system("/usr/bin/clear")
			print("....Running Scan to Metasploitable2 to generate IPS alarms...")
			sleep(3)
			system("/usr/local/bin/nikto-scan.py")
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
