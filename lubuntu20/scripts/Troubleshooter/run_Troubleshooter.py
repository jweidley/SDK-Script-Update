#!/usr/bin/python3
# Purpose: Basic troubleshooting script to verify inter-connectivity
# Version: 0.3
# Modified from: https://github.com/pklimai/pyez-network-testing
########################################################################################
# ChangeLog:
# 0.3: 18May20: Added color to pass/fail
########################################################################################

##########################
# Modules
##########################
from __future__ import print_function
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectTimeoutError
from time import sleep
import sys
import paramiko
from os.path import split, splitext, isfile, join
from os import listdir

##########################
# Variables
##########################
class style:
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

Junos_HOSTS = {
    "vsrx": "192.168.100.1",
}

Linux_HOSTS = {
    "lubuntu": "192.168.100.10",
    "dmz-svr": "192.168.200.10",
}

USER = "juniper"
PASSWD = "juniper123"

# Dynamically find Junos test scripts
junos_script_dir = split(__file__)[0] or "."
for f in listdir(junos_script_dir):
    if isfile(join(junos_script_dir, f)) and f.startswith("junos_") and f.endswith(".py"):
        exec("from %s import *" % splitext(f)[0])

# Dynamically find Linux test scripts
linux_script_dir = split(__file__)[0] or "."
for f in listdir(linux_script_dir):
    if isfile(join(linux_script_dir, f)) and f.startswith("linux_") and f.endswith(".py"):
        exec("from %s import *" % splitext(f)[0])


if __name__ == "__main__":

    print(style.BOLD + "==========================================================================" + style.END)
    print(style.BOLD + " SDK: Automated Troubleshooter" + style.END)
    print(style.YELLOW + "  -- Note: Ensure you have the BASE configuration loaded on the vSRX" + style.END)
    print(style.BOLD + "==========================================================================" + style.END)
    tests_success = 0
    tests_fail = 0

    # Test Linux Hosts
    for host in sorted(Linux_HOSTS.keys()):
        print("Running tests for %s" % host)
        cli = paramiko.client.SSHClient()
        cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            cli.connect(hostname=Linux_HOSTS[host], username=USER, password=PASSWD, timeout=5)
            for name in dir():
                if name.startswith("test_all_"):
                    print("\tRunning %s... " % name, end="")
                    test_result = locals()[name](cli)
                    if test_result:
                        print(style.GREEN + "\tpass" + style.END)
                        tests_success += 1
                    else:
                        print(style.RED + "\t***FAIL***" + style.END)
                        tests_fail += 1

        except Exception as err:
            print("\tCannot connect to device: {0}".format(err))
            sleep(3)
            continue

        cli.close()

    # Test Junos Hosts
    for host in sorted(Junos_HOSTS.keys()):
        print("Running tests for %s" % host)
        try:
            with Device(host=Junos_HOSTS[host], user=USER, passwd=PASSWD, gather_facts=False) as dev:
                for name in dir():
                    if name.startswith("test_%s_" % host):
                        print("\tRunning %s... " % name, end="")
                        test_result = locals()[name](dev)
                        if test_result:
                            print(style.GREEN + "\tpass" + style.END)
                            tests_success += 1
                        else:
                            print(style.RED + "\t***FAIL***" + style.END)
                            tests_fail += 1
        except ConnectError as err:
            print("\tCannot connect to device: {0}".format(err))
            sleep(3)
            continue

        except Exception as err:
            print("\tCannot connect to device: {0}".format(err))
            sleep(3)
            continue


    # Print Trailer Summary
    print("--------")
    print("Network test script finished. Successful tests: %s, failed tests: %s" % (tests_success, tests_fail))
    if tests_fail == 0:
        print(style.GREEN + " All test Passed." + style.END)
    else:
        print(style.RED + "***WARNING***: There were failed tests!" + style.END)

## End of script ##
