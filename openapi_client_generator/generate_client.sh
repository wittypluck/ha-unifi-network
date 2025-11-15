#!/bin/bash

#Remove license (empty):
#Change frequenceGHz type from string to number:
#Change "Port PoE overview" "type" from string to number:
jq 'del(.info.license) 
    | walk(if type == "object" and has("frequencyGHz") 
           then .frequencyGHz = {type:"number", "format": "double"} 
           else . end) 
    | walk(if type == "object" and .type == "integer" and (.enum | type == "array") 
          then .enum |= map(tonumber) 
          else . end)' integration.json > integration-fix.json

#Remove previous client
rm -rf unifi-network-api-client

#Generate new client with post hooks to fix and format code
openapi-python-client generate --path integration-fix.json --output-path unifi-network-api-client --config openapi-generator-config.yaml

#Remove old copy of client (moved under custom_components for HACS)
rm -rf ../custom_components/unifi_network/api_client

#Move new client to HACS-compliant path
mv unifi-network-api-client/unifi_network_api_client ../custom_components/unifi_network/api_client

