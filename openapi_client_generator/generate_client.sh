#!/bin/bash

# Normalize and filter API json
python3 normalize_openapi.py integration.json \
    --output-file integration-fix.json \
    --rename "IP Address selector:IP_Address_selector_2" \
    --filter-tags "Sites" "UniFi Devices" "Clients" \
    --fix-type "frequencyGHz:number"

# Remove previous client
rm -rf unifi-network-api-client

# Generate new client with post hooks to fix and format code
openapi-python-client generate --path integration-fix.json --output-path unifi-network-api-client --config openapi-generator-config.yaml

# Remove old copy of client (moved under custom_components for HACS)
rm -rf ../custom_components/unifi_network/api_client

# Move new client to HACS-compliant path
mv unifi-network-api-client/unifi_network_api_client ../custom_components/unifi_network/api_client
