#############################################################################################
# Purpose: Functions for gathering system information.
# Version: 0.1
#############################################################################################

# Modules
import jxmlease

def test_vsrx_SYSTEM_total_memory_percent_util(dev):
    parser = jxmlease.EtreeParser()
    res = parser(dev.rpc.get_route_engine_information())
    # The 80% threshold is arbitrary and you might want to set different number in your env.
    # Also consider checking control and data plane memory utilization separately

    try:
        return int(res["route-engine-information"]["route-engine"]["memory-system-total-util"]) < 85

    ## Required for EX3400
    except KeyError:
        return int(res["route-engine-information"]["route-engine"]["memory-buffer-utilization"]) < 80

## End of Script ##
