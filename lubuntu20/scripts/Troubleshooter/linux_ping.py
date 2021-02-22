#############################################################################################
# Purpose: Functions for verifying network connectivity
# Version: 0.1
#############################################################################################

# Modules
import re

def format_and_return(lines):
	summLine = re.split(',\s', lines[3])      # split loss line on ,
	rcvdPkts = re.split('\s', summLine[1])    # split to get just the pkt loss percent number
	return int(rcvdPkts[0])

def test_all_NETWORK_ping_lubuntu______________(cli):
	stdin_, stdout_, stderr_ = cli.exec_command("/bin/ping -q -c 3 192.168.100.10", timeout=5)
	stdout_.channel.recv_exit_status()
	lines = stdout_.readlines()
	def_result = format_and_return(lines)
	return(def_result)

def test_all_NETWORK_ping_dmz_svr______________(cli):
	stdin_, stdout_, stderr_ = cli.exec_command("/bin/ping -q -c 3 192.168.200.10", timeout=5)
	stdout_.channel.recv_exit_status()
	lines = stdout_.readlines()
	def_result = format_and_return(lines)
	return(def_result)

def test_all_NETWORK_ping_metasploitable_______(cli):
	stdin_, stdout_, stderr_ = cli.exec_command("/bin/ping -q -c 3 192.168.100.20", timeout=5)
	stdout_.channel.recv_exit_status()
	lines = stdout_.readlines()
	def_result = format_and_return(lines)
	return(def_result)

## End of script ##
