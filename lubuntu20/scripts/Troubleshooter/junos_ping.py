#############################################################################################
# Purpose: Functions for verifying network connectivity
# Version: 0.1
#############################################################################################

def test_vsrx_NETWORK_ping_lubuntu____________(dev):
    res = dev.rpc.ping(count="5", rapid=True, host="192.168.100.10")
    # We allow 1 of 5 packets to be lost in this test
    return int(res.findtext("probe-results-summary/packet-loss")) <= 1

def test_vsrx_NETWORK_ping_dmz_server_________(dev):
    res = dev.rpc.ping(count="5", rapid=True, host="192.168.200.10")
    # We allow 1 of 5 packets to be lost in this test
    return int(res.findtext("probe-results-summary/packet-loss")) <= 1

def test_vsrx_NETWORK_ping_metasploitable_____(dev):
    res = dev.rpc.ping(count="5", rapid=True, host="192.168.100.20")
    # We allow 1 of 5 packets to be lost in this test
    return int(res.findtext("probe-results-summary/packet-loss")) <= 1

def test_vsrx_NETWORK_ping_google_by_IP_______(dev):
    res = dev.rpc.ping(count="5", rapid=True, host="8.8.8.8")
    # We allow 1 of 5 packets to be lost in this test
    return int(res.findtext("probe-results-summary/packet-loss")) <= 1

def test_vsrx_NETWORK_ping_google_by_NAME_____(dev):
    res = dev.rpc.ping(count="5", rapid=True, inet=True, host="www.google.com")
    # We allow 1 of 5 packets to be lost in this test
    return int(res.findtext("probe-results-summary/packet-loss")) <= 1

## End of Script ##
