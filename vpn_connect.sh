#!/bin/bash

# Variables
OVPN_CONFIG="vpn_itb/config/itb-2022-mac.ovpn"
CA_CERT="vpn_itb/config/ca.crt"
CLIENT_CERT="vpn_itb/config/client-vpn.crt"
CLIENT_KEY="vpn_itb/config/client-vpn.key"
TEST_URL="https://elisa.itb.ac.id/"

# Function to connect to the VPN
connect_vpn() {
    echo "Connecting to VPN..."    
    sudo openvpn3 config-remove --config MAS-LLM_ITB
    sudo openvpn3 config-import --config /home/nafimulyoo/TA/elisa-smart-analysis/vpn_itb/itb-2022-mac.ovpn --name MAS-LLM_ITB
    sudo openvpn3 config-manage --config MAS-LLM_ITB --allow-compression yes
    sudo openvpn3 session-start --config MAS-LLM_ITB
         
    VPN_PID=$!
    sleep 10  # Wait for the VPN connection to establish
}

# Function to test the connection
test_connection() {
    echo "Testing connection to $TEST_URL..."
    ping -c 4 elisa.itb.ac.id
}

# Main script execution
connect_vpn
test_connection

# Clean up
echo "Disconnecting from VPN..."
sudo kill $VPN_PID