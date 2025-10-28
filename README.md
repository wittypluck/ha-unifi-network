# Unifi Network (custom integration)

Home Assistant custom integration for UniFi Network that uses UniFi's official Integration API. It discovers UniFi devices and connected clients, exposes presence (device trackers), and publishes diagnostic sensors for devices and radios.

## What this provides

- Local polling against the UniFi Network Integration API (no cloud)
- Config flow in the UI (no YAML)
- Entity categories marked as Diagnostic
- Two platforms enabled by default:
  - device_tracker
  - sensor

### Entities created

1. Device trackers

- UniFi device tracker: Reports home/not_home based on device state (ONLINE/OFFLINE). Attributes include ip, mac, source_type=router.
- UniFi client tracker: Reports home when the client is currently connected; not_home otherwise. Attributes include ip, mac, source_type=router.

1. Device sensors

- Device statistics (per device):
  - uptime_sec (s)
  - load_average_1_min
  - load_average_5_min
  - load_average_15_min
  - cpu_utilization_pct (%)
  - memory_utilization_pct (%)
- Uplink statistics (per device):
  - uplink_rx_rate_bps (suggested display as Mbps)
  - uplink_tx_rate_bps (suggested display as Mbps)
- Radio statistics (per device, per radio frequency):
  - tx_retries_pct (%) — one sensor per available radio frequency (e.g., 2.4, 5, 6 GHz)

Update interval: 30s by default.

## Requirements

- A UniFi Network Application that exposes the Integration API (UniFi OS / Network Application with Integrations). You will need an API Key created in UniFi Network.
- Home Assistant with access to your UniFi Network Application over your LAN.

## Installation

Manual install:

1. Copy the `unifi_network` folder into your Home Assistant config directory under `custom_components` (final path: `<config>/custom_components/unifi_network`).
1. Restart Home Assistant.

## Configuration (via UI)

1. In Home Assistant, go to Settings → Devices & Services → Add Integration → search for "Unifi Network (Local API)".

1. Enter the settings (Base URL: for example `https://<unifi-host-or-ip>/proxy/network/integration`; API Key: create one from UniFi Network → Settings → Integrations → Add Integration → API Key).

1. Select the site you want to add when prompted.

1. Choose which features to enable:
   - **Track Devices**: Monitor UniFi network devices (switches, access points, gateways)
   - **Track Clients**: Monitor connected clients (computers, phones, IoT devices)
   - You can enable one or both features based on your needs.

The integration will then create device trackers and sensors for your selected features. All devices and clients are automatically fetched using pagination to ensure complete discovery.

## Notes and troubleshooting

- SSL: If you use self-signed certificates, ensure your Home Assistant host trusts the UniFi certificate, or use an HTTPS setup with a valid cert.
- Permissions: The API Key should have sufficient privileges for read access to devices, clients, and statistics.
- Presence logic:
  - Devices: ONLINE → home, OFFLINE → not_home.
  - Clients: Present in the “connected clients” list → home; otherwise not_home.
- Radio sensors appear only when the device exposes radio interface statistics.

## Development

- Code structure
  - `unifi_network/` contains the custom component logic, coordinators, and entity platforms.
  - `unifi_network/api_client/` contains the generated UniFi Network Integration API client and models.
  - Update cadence is controlled in `const.py` (DEFAULT_UPDATE_INTERVAL).

- Running locally
  - This is a regular Home Assistant custom component; install as described above and restart HA to load changes.

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
