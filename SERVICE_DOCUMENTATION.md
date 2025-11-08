# Remove Stale Clients Service

This document describes the `remove_stale_clients` service that was added to the UniFi Network integration.

## Purpose

The `remove_stale_clients` service removes devices from the Home Assistant device registry that are no longer present in the UniFi Network's known clients list. This helps keep the device registry clean by removing devices for clients that are no longer connecting to your network.

## Service Details

**Service Name:** `unifi_network.remove_stale_clients`

**Description:** Remove devices from the Home Assistant device registry that are no longer in the known clients list

## Parameters

### config_entry_id (optional)

- **Type:** string
- **Required:** No
- **Description:** The config entry ID (UUID) or name/title to remove stale clients from. If not provided, all UniFi Network integrations will be processed.
- **Format:** Either a UUID string (e.g., `01234567-89ab-cdef-0123-456789abcdef`) or the integration name (e.g., `"Unifi: Main Site"`)

#### How to find your config entry identifier:

**Option 1: Use the Integration Name (Recommended - User Friendly)**
- Go to Settings → Devices & Services
- Find your "Unifi Network" integration
- Use the exact title shown (e.g., "Unifi: Main Site", "Unifi: Guest Network")
- **Note:** If multiple integrations have the same name, all matching integrations will be processed

**Option 2: Use the Config Entry ID (UUID)**
1. **Via Home Assistant UI:**
   - Go to Settings → Devices & Services
   - Find your "Unifi Network" integration
   - Click on the integration entry
   - The config_entry_id appears in the browser URL: `/config/integrations/integration/YOUR_CONFIG_ENTRY_ID`

2. **Via Developer Tools:**
   - Go to Developer Tools → States
   - Find any entity from your UniFi Network integration
   - Click on the entity to see details
   - Look for the `config_entry_id` in the entity attributes

## Usage Examples

### Remove stale clients from all UniFi Network integrations
```yaml
service: unifi_network.remove_stale_clients
```

### Remove stale clients from a specific integration by name
```yaml
service: unifi_network.remove_stale_clients
data:
  config_entry_id: "Unifi: Main Site"
```

### Remove stale clients from a specific integration by ID
```yaml
service: unifi_network.remove_stale_clients
data:
  config_entry_id: "01234567-89ab-cdef-0123-456789abcdef"
```

## How It Works

1. The service identifies all UniFi Network integration instances (or a specific one if `config_entry_id` is provided)
2. For each integration, it gets the list of currently known clients from the UniFi Network coordinator
3. It scans the Home Assistant device registry for devices associated with the integration
4. Any device that represents a client but is no longer in the known clients list is removed from the device registry
5. The service logs the number of devices removed and processed

## When to Use

This service is useful in scenarios such as:
- After guests have left and their devices should be removed from Home Assistant
- When you want to clean up old devices that no longer connect to your network
- As part of regular maintenance to keep your device registry tidy
- After network topology changes where certain client devices are no longer relevant

## Safety

The service only removes client devices (not UniFi network equipment like access points, switches, etc.) and only removes devices that are definitively no longer in the known clients list. It includes extensive logging to show what devices are being removed and why.

## Integration with Home Assistant Best Practices

This service follows Home Assistant best practices by:
- Providing proper service definition in `services.yaml`
- Including proper translations in `strings.json`
- Using voluptuous for parameter validation
- Registering the service only once globally (not per config entry)
- Properly cleaning up the service when the last integration instance is unloaded
- Using appropriate logging levels (info for actions, debug for details)
- Following naming conventions and code organization standards
- Separating service code into a dedicated `services.py` module for better organization