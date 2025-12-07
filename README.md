# Unifi Network (custom integration)

[![Tests](https://github.com/wittypluck/ha-unifi-network/actions/workflows/tests.yml/badge.svg)](https://github.com/wittypluck/ha-unifi-network/actions/workflows/tests.yml)
[![Code Quality](https://github.com/wittypluck/ha-unifi-network/actions/workflows/quality.yml/badge.svg)](https://github.com/wittypluck/ha-unifi-network/actions/workflows/quality.yml)

Home Assistant custom integration for UniFi Network that uses UniFi's official Integration API. It discovers UniFi devices and connected clients, exposes presence detection (device trackers), and provides comprehensive monitoring sensors and control buttons.

## What this provides

- Local polling against the UniFi Network Integration API (no cloud)
- Config flow in the UI (no YAML required)
- Automatic device and client discovery with pagination support
- Selective feature enabling (devices and/or clients)
- Entity categories appropriately marked as Diagnostic or Config
- Service for cleaning up stale client devices from device registry
- Four platforms:
  - **device_tracker** - Presence detection for clients
  - **sensor** - Monitoring and diagnostics for devices
  - **button** - Device and port controls
  - **update** - Firmware update information

### Entities created

#### Device Trackers

- **UniFi Client Tracker**: Reports `home` when client is currently connected, `not_home` otherwise. Attributes include IP address, MAC address, last seen timestamp, connected at timestamp (when available), and `source_type=router`. Automatically created for all discovered clients when client tracking is enabled.

#### Device Sensors

- **Device State**: Current operational state (Online, Offline, etc.)
- **System Statistics** (per device):
  - Uptime (timestamp showing when device started)
  - Load Average (1, 5, and 15 minute averages)
  - CPU Utilization (%)
  - Memory Utilization (%)
  
- **Uplink Statistics** (per device):
  - Uplink RX Rate (bps, suggested display as Mbps)
  - Uplink TX Rate (bps, suggested display as Mbps)
  
- **Radio Statistics** (per device, per available radio frequency):
  - TX Retries (%) — created for each available radio frequency (e.g., 2.4GHz, 5GHz, 6GHz)
  
- **Port Statistics** (per device, per physical port):
  - Port State (Up, Down, etc.) with additional attributes for port details
  
- **PoE Port Statistics** (per device, per PoE-capable port):
  - PoE State (Providing Power, Off, etc.) with PoE standard and type information

#### Device Buttons

- **PoE Port Power Cycle** (per device, per PoE-capable port): Triggers power cycle action on PoE ports. Button is automatically available only for ports with PoE capability.
- **Restart Device** (per device): Triggers a restart action on the device. Button is only available when device is online.

#### Update Entities

- **Firmware Update** (per device): Shows current firmware version and indicates if firmware updates are available. Displays "Unknown" for latest version when an update is available (UniFi API doesn't provide specific version information). Note: Firmware installation through Home Assistant is not supported - use the UniFi Network Application for updates.

#### Services

- **Remove Stale Clients** (`unifi_network.remove_stale_clients`): Removes devices from the Home Assistant device registry that are no longer in the known clients or devices list. Useful for cleaning up devices that were previously tracked but are no longer present in the UniFi network. Can target specific config entries or process all UniFi Network integrations.

**Update interval**: 30 seconds by default.

### Future Capabilities

The integration uses a comprehensive API client that supports additional UniFi Network features that could be implemented in future versions:

- Hotspot voucher management (create, delete, monitor vouchers)
- Guest access controls and authorization
- Advanced device and client actions beyond PoE control
- VPN and Teleport client monitoring

Current implementation focuses on core monitoring and basic device control functionality.

## Requirements

- **UniFi Network Application**: UniFi OS / Network Application version that supports the Integration API
  - Must have "Integrations" feature available in Network settings
  - API Key generation capability:
    - **UniFi OS 4.4.x and earlier**: UniFi Network → Settings → Control Plane → Integrations → Create API key
    - **UniFi OS 5.0.x and later**: UniFi Network → Integrations (next to Settings at bottom left) → Create New Api Key
- **Network Access**: Home Assistant must have network access to your UniFi Network Application
  - Typically runs on port 443 (HTTPS) or 8443
  - Integration API endpoint: `/proxy/network/integration`
- **Supported UniFi Devices**: Any UniFi network devices managed by your Network Application
  - Switches, Access Points, Gateways, etc.
  - PoE functionality requires PoE-capable switch ports

## Installation

> Note: HACS installation via the default store is not available yet. You can install manually (see below). If you want to use HACS today, add this repository as a Custom Repository in HACS.

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=wittypluck&repository=ha-unifi-network&category=integration)

1. Ensure you have [HACS](https://hacs.xyz/) installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Open HACS in Home Assistant
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add the repository URL: `https://github.com/wittypluck/ha-unifi-network`
   - Select category: "Integration"
   - Click "Add"
3. Search for "Unifi Network (Local API)" in HACS
4. Click "Download"
5. Restart Home Assistant
6. Go to **Settings → Devices & Services → Add Integration** and search for "Unifi Network (Local API)"

### Manual Installation

1. Copy the `custom_components/unifi_network` folder from this repository to your Home Assistant config directory under `custom_components` (final path: `<config>/custom_components/unifi_network`).
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for "Unifi Network (Local API)".

## Configuration (via UI)

1. In Home Assistant, go to **Settings → Devices & Services → Add Integration** → search for "**Unifi Network (Local API)**".

2. **Connection Setup**: Enter your UniFi Network API credentials:
   - **Base URL**: Your UniFi Network Integration API endpoint
     - Format: `https://<unifi-host-or-ip>/proxy/network/integration`
     - Example: `https://192.168.1.1/proxy/network/integration`
   - **API Key**: Create an API key in the UniFi Network Application:
     - **UniFi OS 4.4.x and earlier**: UniFi Network → Settings → Control Plane → Integrations → Create API key
     - **UniFi OS 5.0.x and later**: UniFi Network → Integrations (next to Settings at bottom left) → Create New Api Key
   - **Verify SSL Certificate**: Enable for production, disable for self-signed certificates

3. **Site Selection**: Choose which UniFi site to monitor from the automatically discovered list.

4. **Feature Selection**: Choose which features to enable:
   - **Unifi Devices sensors and actions**: Monitor UniFi network infrastructure devices (switches, access points, gateways, etc.) with comprehensive sensors, buttons, and firmware update information
   - **Track Clients**: Monitor connected client devices (computers, phones, IoT devices, etc.) with device tracker entities
   - You can enable one or both features based on your monitoring needs

The integration will automatically discover all devices and clients using API pagination to ensure complete coverage. Entities are created dynamically based on device capabilities (e.g., PoE sensors and buttons only appear for ports with PoE support, radio sensors only for devices with wireless radios).

## Notes and troubleshooting

- **SSL Certificates**: If using self-signed certificates, disable SSL verification in the integration settings or ensure your Home Assistant host trusts the UniFi certificate.
- **API Permissions**: The API Key should have sufficient privileges for read access to devices, clients, statistics, and port control actions.
- **Presence Detection Logic**:
  - **Clients**: Present in connected clients list → `home`, otherwise → `not_home`
- **Dynamic Entity Creation**:
  - Radio sensors only appear for devices that expose radio interface statistics (Access Points, Gateways with Wi-Fi)
  - Port sensors are created for all physical ports on devices with port interfaces (Switches, Gateways)
  - PoE sensors and buttons only appear for ports with PoE capability
  - Client trackers are created for all connected clients and automatically updated as new clients connect
  - Update entities show firmware information for all devices with available firmware data
- **Device Capabilities**: Different UniFi devices expose different sensor sets based on their hardware capabilities (e.g., switches vs access points vs gateways).
- **Entity Organization**:
  - Device entities are grouped under their respective UniFi device in the Device Registry
  - Client entities are grouped under their respective client device
  - All entities use the device/client name as the device name with specific sensor names
  - Entity categories are set appropriately (Diagnostic for monitoring, Config for controls)
- **Service Usage**: Use the `unifi_network.remove_stale_clients` service to clean up the device registry when clients are no longer present in your network

## Development

### Project Structure

- **`unifi_network/`**: Main integration code
  - Core integration logic, coordinators, and entity platforms
  - Entity platforms: `device_tracker.py`, `sensor.py`, `button.py`, `update.py`
  - Configuration flow: `config_flow.py`
  - Data coordinators: `coordinator.py`
  - Device/client wrappers: `unifi_device.py`, `unifi_client.py`
  - Services: `services.py` (stale client cleanup)
  
- **`unifi_network/api_client/`**: Generated API client (excluded from linting/formatting)
  - Auto-generated from UniFi Network Integration API OpenAPI specification
  - Models, API endpoints, and type definitions
  - Located in `openapi_client_generator/` for regeneration scripts

- **`unifi_network/translations/`**: Internationalization files
  - Entity names, configuration flow text
  - Currently supports English (`en.json`)

### Configuration

- **Update interval**: Controlled by `DEFAULT_UPDATE_INTERVAL` in `const.py` (30 seconds)
- **Platforms**: Defined in `PLATFORMS` in `const.py` (sensor, device_tracker, button, update)
- **Domain**: `unifi_network`
- **Services**: `remove_stale_clients` for device registry cleanup

### Local Development

This is a standard Home Assistant custom component. For development:

1. Install in Home Assistant as described above
2. Make code changes
3. Restart Home Assistant to reload the integration
4. Use Home Assistant logs to debug issues

## Code style and formatting

This project uses Ruff for both formatting and linting, aligned with Home Assistant Core's standards:

- Formatting: Black-compatible via `ruff format` with a line length of 88.
- Imports: Sorted via Ruff's import sorter (`I`).
- Lint rules: A pragmatic selection similar to Home Assistant Core (see `pyproject.toml`).
- Generated code is excluded from lint/format to avoid churn: `openapi_client_generator/` and `unifi_network/api_client/`.

Editor setup (VS Code): The workspace sets Ruff as the default Python formatter and organizes imports on save. You can also install the "Ruff" extension by Astral.

Quick commands (optional):

```bash
# Install Ruff (user env or venv)
pip install ruff

# Format code
ruff format

# Lint and auto-fix safe issues
ruff check --fix

# Enable pre-commit hooks (recommended)
pip install pre-commit
pre-commit install
```

## Disclaimer

This project is not affiliated with Ubiquiti Inc. Use at your own risk.
