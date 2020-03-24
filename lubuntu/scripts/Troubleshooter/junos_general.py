#############################################################################################
# Purpose: Functions for gathering information on system functions
# Version: 0.1
#############################################################################################

# Modules
import jxmlease

def test_vsrx_SYSTEM_junos_version_193r1______(dev):
    parser = jxmlease.EtreeParser()
    res = parser(dev.rpc.get_software_information())
    return res["software-information"]["junos-version"] == "19.3R1.8"


def test_vsrx_SYSTEM_chassis_alarms___________(dev):
    rpc_result = dev.rpc.get_alarm_information()
    return rpc_result.find("alarm-summary/no-active-alarms") is not None


def test_vsrx_SYSTEM_system_alarms____________(dev):
    rpc_result = dev.rpc.get_system_alarm_information()
    return rpc_result.find("alarm-summary/no-active-alarms") is not None


def test_vsrx_SYSTEM_core_dumps_______________(dev):
    rpc_result = dev.rpc.get_system_core_dumps()
    return rpc_result.find("directory/file-information") is None

## End of Script ##
