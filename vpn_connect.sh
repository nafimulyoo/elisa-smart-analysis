#!/bin/bash

# Variables
TEST_URL="https://elisa.itb.ac.id/"
# Auth variable from ENV

# Create TUN device
[ -c /dev/net/tun ] || mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun


# Function to connect to the VPN
connect_vpn() {
    echo "Connecting to VPN..."    
    openvpn3 config-remove --config MAS-LLM_ITB
    openvpn3 config-import --config ./vpn-config/itb-2022-mac.ovpn --name MAS-LLM_ITB
    openvpn3 config-manage --config MAS-LLM_ITB --allow-compression yes
    openvpn3 session-start --config MAS-LLM_ITB
    
    VPN_PID=$!
    sleep 10  # Wait for the VPN connection to establish
}

# Function to test the connection
# test_connection() {
#     echo "Testing connection to $TEST_URL..."
#     ping -c 4 elisa.itb.ac.id
# }

# Main script execution
connect_vpn
# test_connection

# Clean up
# echo "Disconnecting from VPN..."
# sudo kill $VPN_PID