#!/usr/bin/python3
# Purpose: Common SDK functions
# Version: 0.1
# Author: John Weidley
#########################################################################################
# ChangeLog
# 0.1: 23Jan21: Initial Release
#########################################################################################

###################
# Dependencies
###################
import yaml

#################################################################################################################
# readConfig Function:
# Read in the main configuration file and return to the main script as a dictionary
#################################################################################################################
def readConfig():
    try:
        with open("/etc/sdk/sdk.conf", "r") as cfgFile:
            print("** Reading /etc/sdk/sdk.conf")
            config = yaml.safe_load(cfgFile)
            return config
    except Exception as error:
        print("\nCould not find or read SDK configuration file!!!")
        print("ERROR: Reading configuration file: {0}\n".format(error))
        exit()

#################################################################################################################
# checkConfig Function:
# Verify that the key and value exists and returns string to the main script.
#################################################################################################################
def checkConfig(config, key, value):
    if key in config:
        if ((config[key] is not None) and (value in config[key])) :
            return config[key][value]
        else:
            print("ERROR: Couldnt find \'" + key + ":" + value + "\' in config file...Exiting!")
            exit()
    else:
        print("WARNING: Couldnt find \'" + key + "\' in the config file...Exiting!")
        exit()

#################################################################################################################
# checkConfigSRX Function:
# Requires the verification of multiple required configuration values. Results are returned as a dictionary to
# the main script.
#################################################################################################################
def checkConfigSRX(config, key):
    if ((key == "vsrx") and (key in config)):
        srxCreds = dict();
        required = set(['user', 'passwd', 'trust_ip'])
        if ((config[key] is not None) and (required.issubset(config[key]))):
            srxCreds['user'] = config[key]["user"]
            srxCreds['passwd'] = config[key]["passwd"]
            srxCreds['vsrx'] = config[key]["trust_ip"]
            return srxCreds
        else:
            print("ERROR: MISSING required credential information..!")
            print("- Ensure \'vsrx: user, passwd, trust_ip\' options are set.")
            exit()
    else:
        print("ERROR: Couldnt find \'vsrx\' in config file...Exiting!")
        exit()

## End of File ##
