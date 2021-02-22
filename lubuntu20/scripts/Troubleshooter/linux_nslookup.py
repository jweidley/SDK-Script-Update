#############################################################################################
# Purpose: Functions for verifying network connectivity
# Version: 0.1
#############################################################################################

def test_all_NETWORK_dnslookup_google__________(cli):
    stdin_, stdout_, stderr_ = cli.exec_command("/usr/bin/host -W2 -ta www.google.com")
    stdout_.channel.recv_exit_status()
    
    # The exit status is opposite (1=pass,0=fail), this reverses it.
    if stdout_.channel.recv_exit_status() == 1:
        dns_result = 0
    else:
        dns_result = 1
    return(dns_result)

## End of script ##
