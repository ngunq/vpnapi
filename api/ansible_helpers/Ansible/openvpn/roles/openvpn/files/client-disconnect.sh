#!/bin/bash

CONF_FILE="/etc/openvpn/conf.json"

function get_server_ip() {
    local server_ip
    server_ip=$(jq -r '.nodes[0].serverHostname' "$CONF_FILE")
    echo "$server_ip"
}

function get_secret() {
    local secret
    secret=$(jq -r '.secret' "$CONF_FILE")
    echo "$secret"
}

function send_api_request() {
    local api_url=$1
    local secret=$2
    local username=$3

    # Log the username and redirect the output to the log file
    echo "Disconnecting: $username" >> /etc/openvpn/openvpn_auth.log


    # Create the API request payload
    local payload="{\"secret\":\"$secret\",\"username\":\"$username\"}"

    # Send the API request
    response=$(curl --max-time 2 -X POST \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$api_url")

    # Check if the curl command was successful
    if [ $? -ne 0 ]; then
        echo "Curl failed with error code $?" >> /etc/openvpn/openvpn_auth.log
    else
        echo "API response: $response" >> /etc/openvpn/openvpn_auth.log
    fi
    #exit 0
}

# Script entry point for client-disconnect
function on_disconnect() {
    local username=$username

    local server_ip=$(get_server_ip)
    local secret=$(get_secret)
    local api_url="http://$server_ip/api/OpenVPN/disconnect"

    send_api_request "$api_url" "$secret" "$username"
}

# Call the disconnect function
on_disconnect