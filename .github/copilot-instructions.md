# Copilot Instructions for ha-unifi-network

## Repository Overview

This is a **Home Assistant custom integration** for UniFi Network that provides local polling against the UniFi Network Integration API. The project is approximately 1MB in size and consists of ~1,800 lines of Python code (excluding auto-generated API client).

**Key Technologies:**
- **Language:** Python 3.12+
- **Framework:** Home Assistant Custom Component
- **API Client:** Auto-generated OpenAPI client (excluded from linting)
- **Linting/Formatting:** Ruff (Black-compatible, 88 char line length)

**Main Features:**
- Device and client discovery with pagination
- Device tracker (presence detection)
- Sensors (device state, system stats, uplink stats, radio stats, port stats, PoE stats, client connection)
- Buttons (PoE port power cycle, device actions)
- Config flow (no YAML required)

## Home Assistant Standards

**CRITICAL:** This is a **Home Assistant custom integration**. All code changes MUST follow Home Assistant coding standards and best practices as documented in the [Home Assistant Developer Documentation](https://developers.home-assistant.io/).

**Key Home Assistant Requirements:**
- Use async/await patterns (all I/O operations must be async)
- Use `CoordinatorEntity` for entities that poll data
- Implement proper `DeviceInfo` with identifiers and connections
- Use `config_flow` for UI-based configuration (no YAML)
- Follow entity naming conventions (`_attr_has_entity_name = True`)
- Set appropriate entity categories (DIAGNOSTIC, CONFIG)
- Handle exceptions gracefully and log appropriately
- Use Home Assistant helpers (`dt_util`, `device_registry`, etc.)
- Respect the integration manifest structure (`manifest.json`)
- Use translation files (`strings.json`, `translations/*.json`)

**Integration Structure Requirements:**
- Entry point: `async_setup_entry()` in `__init__.py`
- Cleanup: `async_unload_entry()` in `__init__.py`
- Platforms loaded via `async_forward_entry_setups()`
- Data stored in `hass.data[DOMAIN][entry.entry_id]`
- Coordinators for data fetching (not direct API calls in entities)

**Reference Documentation:**
- Integration setup: https://developers.home-assistant.io/docs/creating_component_index
- Config flow: https://developers.home-assistant.io/docs/config_entries_config_flow_handler
- Entity platform: https://developers.home-assistant.io/docs/core/entity
- Data coordinator: https://developers.home-assistant.io/docs/integration_fetching_data

## Project Architecture

### Directory Structure

```
/
├── .github/                    # GitHub metadata (copilot instructions)
├── .vscode/                    # VS Code settings (Ruff formatter)
├── openapi_client_generator/   # API client generation scripts (EXCLUDED from linting)
│   ├── generate_client.sh     # Regenerates API client from OpenAPI spec
│   └── integration.json       # UniFi Network Integration API spec
├── unifi_network/             # Main integration code
│   ├── api_client/            # Auto-generated API client (EXCLUDED from linting)
│   ├── translations/          # i18n files (en.json)
│   ├── __init__.py            # Integration setup/teardown (59 lines)
│   ├── api_helpers.py         # Pagination helper (65 lines)
│   ├── button.py              # Button platform (394 lines)
│   ├── config_flow.py         # UI configuration flow (150 lines)
│   ├── const.py               # Constants (DOMAIN, PLATFORMS, update interval)
│   ├── coordinator.py         # Data coordinators for devices & clients (234 lines)
│   ├── core.py                # Core integration class (51 lines)
│   ├── device_tracker.py      # Device tracker platform (110 lines)
│   ├── sensor.py              # Sensor platform (602 lines)
│   ├── unifi_client.py        # Client data wrapper (63 lines)
│   ├── unifi_device.py        # Device data wrapper (37 lines)
│   ├── manifest.json          # Integration manifest
│   ├── strings.json           # Translation strings
│   └── icons.json             # Custom icons
├── .gitignore                 # Standard Python gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks (ruff-format, ruff)
├── pyproject.toml             # Ruff configuration
└── README.md                  # Project documentation
```

### Key Configuration Files

- **`pyproject.toml`**: Ruff linting and formatting configuration (target Python 3.12, line length 88)
- **`.pre-commit-config.yaml`**: Pre-commit hooks using ruff-pre-commit v0.6.9
- **`.vscode/settings.json`**: Format on save with Ruff, organize imports on save
- **`unifi_network/manifest.json`**: Home Assistant integration manifest (version, domain, requirements)

### Source File Summary

**Core Integration Files:**
- `__init__.py`: Entry point, async_setup_entry, async_unload_entry, device removal
- `core.py`: UnifiNetworkCore class, initializes API client and coordinators
- `const.py`: DOMAIN="unifi_network", PLATFORMS=["sensor", "device_tracker", "button"], DEFAULT_UPDATE_INTERVAL=30

**Data Management:**
- `coordinator.py`: UnifiDeviceCoordinator and UnifiClientCoordinator (fetch data every 30s)
- `unifi_device.py`: UnifiDevice wrapper combining overview, statistics, and details
- `unifi_client.py`: UnifiClient wrapper combining overview and details
- `api_helpers.py`: fetch_all_pages() for paginated API calls

**Entity Platforms:**
- `sensor.py`: Device sensors (state, uptime, load, CPU, memory, uplink rates, radio stats, port states, PoE states), client sensors (connection state, connected_at)
- `device_tracker.py`: Device and client presence detection (home/not_home)
- `button.py`: PoE port power cycle buttons, device action buttons

**Configuration:**
- `config_flow.py`: Multi-step config flow (credentials → site selection → feature selection)

## Build and Validation Commands

### Prerequisites

**ALWAYS install Ruff before running any linting or formatting:**
```bash
pip install ruff
```

### Linting (ALWAYS run before committing)

```bash
ruff check
```
- Runs in < 5 seconds
- Checks all Python files except `openapi_client_generator/` and `unifi_network/api_client/`
- Auto-fixes safe issues with: `ruff check --fix`
- Reports: E/F/W (pycodestyle), I (import sorting), UP (pyupgrade), B (bugbear), and many more

### Formatting (ALWAYS run before committing)

```bash
ruff format
```
- Runs in < 5 seconds
- Black-compatible formatting with 88 character line length
- Formats all Python files except generated API client
- Check without modifying: `ruff format --check`

### Pre-commit Hooks (Optional but Recommended)

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
- **NOTE:** Pre-commit setup may timeout on first run due to network issues downloading dependencies
- If pre-commit fails with timeout, manually run `ruff format` and `ruff check --fix` instead
- Pre-commit runs automatically on git commit after installation

### No Automated Tests

**This repository has NO test suite.** Do not attempt to run pytest or any test commands. Validation is done through:
1. Ruff linting (code quality)
2. Ruff formatting (code style)
3. Manual testing in Home Assistant environment

### No Build Step

This is a pure Python integration with no build/compilation step. The code is used directly by Home Assistant.

## Development Workflow

### Making Code Changes

**IMPORTANT:** When making any code changes, ensure they follow Home Assistant coding standards and best practices. Reference the [Home Assistant Developer Documentation](https://developers.home-assistant.io/) for guidance on integration structure, async patterns, entity implementation, and data coordinators.

1. **ALWAYS run linting BEFORE making changes** to understand baseline:
   ```bash
   ruff check
   ruff format --check
   ```

2. Make your changes to files in `unifi_network/` (NOT in `api_client/` or `openapi_client_generator/`)

3. **ALWAYS run linting AFTER changes:**
   ```bash
   ruff check --fix
   ruff format
   ```

4. **Verify no errors:**
   ```bash
   ruff check  # Should output: "All checks passed!"
   ```

### File Modification Guidelines

**DO modify:**
- Any `.py` file in `unifi_network/` root (excluding `api_client/`)
- Translation files in `unifi_network/translations/`
- Documentation files (README.md, etc.)

**DO NOT modify:**
- Files in `unifi_network/api_client/` (auto-generated)
- Files in `openapi_client_generator/unifi-network-api-client/` (auto-generated)
- `pyproject.toml` (unless changing lint rules, which is rare)

**Regenerating API Client (rare):**
If UniFi API spec changes, run:
```bash
cd openapi_client_generator
./generate_client.sh
```
This requires `openapi-python-client` and `jq` installed. **Only do this if explicitly asked.**

## Code Style Guidelines

### Import Organization

Ruff automatically organizes imports. The standard order is:
1. `from __future__ import annotations` (if using type hints)
2. Standard library imports
3. Third-party imports (homeassistant, etc.)
4. Local imports (relative imports from this integration)

### Type Hints

- Use modern type hints with `from __future__ import annotations`
- Use `| None` instead of `Optional[T]`
- Use `dict[str, Any]` instead of `Dict[str, Any]`

### Entity Naming Conventions

- Entity unique IDs: `f"unifi_device_{device_id}_{description.key}"`
- Entity classes: `Unifi{Type}{Purpose}` (e.g., `UnifiDeviceStateSensor`)
- Use `_attr_has_entity_name = True` for entity name inheritance
- Mark diagnostic sensors: `_attr_entity_category = EntityCategory.DIAGNOSTIC`
- Mark config entities: `_attr_entity_category = EntityCategory.CONFIG`

### Home Assistant Patterns

- Use `CoordinatorEntity` for entities that update via coordinator
- Use `DeviceInfo` with `identifiers={(DOMAIN, device_id)}` and `connections={(CONNECTION_NETWORK_MAC, mac)}`
- Access coordinator data via `self.coordinator.data` or custom getters
- Handle `UNSET` values from API client (check `value is UNSET`)

## Common Issues and Solutions

### Issue: Ruff reports "Line too long"
**Solution:** Ruff format handles line length automatically. Run `ruff format`.

### Issue: Import sorting errors
**Solution:** Run `ruff check --fix` to auto-fix import order.

### Issue: "Cannot import from api_client"
**Cause:** API client might not be generated or corrupted.
**Solution:** Verify `unifi_network/api_client/` exists and contains Python files. If missing, ask maintainer to regenerate.

### Issue: VS Code not formatting on save
**Solution:** Install "Ruff" extension by Astral and reload window. Settings are already configured in `.vscode/settings.json`.

### Issue: Pre-commit timeout
**Solution:** This is a known network issue. Skip pre-commit and run `ruff format` and `ruff check --fix` manually.

## CI/CD Information

**There are NO GitHub Actions workflows** in this repository. All validation is manual:
- Run `ruff check` before committing
- Run `ruff format` before committing
- Test in Home Assistant development environment

## Entity Platforms Deep Dive

### Sensor Platform (`sensor.py`)

**Device Sensors:**
- State sensor (device online/offline)
- System statistics (uptime, load_average_1/5/15, cpu_utilization, memory_utilization)
- Uplink statistics (uplink_rx_rate, uplink_tx_rate in bps)
- Radio statistics (per radio frequency: tx_retries percentage)
- Port overview sensors (per port: state)
- PoE port sensors (per PoE port: poe_state)

**Client Sensors:**
- Connection state (Connected/Disconnected)
- Connected at timestamp

**Key Classes:**
- `UnifiSensorEntityDescription`: Base description with `sensor_type` reference
- `UnifiDeviceSensor`: Base class for device sensors
- `UnifiDeviceStatisticSensor`: Reads from `device.latest_statistics`
- `UnifiDeviceStateSensor`: Reads from `device.overview.state`
- `UnifiClientSensor`: Base class for client sensors

### Device Tracker Platform (`device_tracker.py`)

- `UnifiClientTracker`: Reports `home` when client is in connected clients list, `not_home` otherwise
- Sets `source_type = SourceType.ROUTER`

### Button Platform (`button.py`)

- `UnifiDevicePortPoeButton`: Power cycle PoE ports (one button per PoE-capable port)
- `UnifiDeviceActionButton`: Trigger device actions (locate, restart, etc.)
- Buttons use `execute_port_action` and `execute_device_action` API calls

## Debugging Tips

### Enable Debug Logging

Add to Home Assistant `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    custom_components.unifi_network: debug
```

### Common Log Messages

- `"Fetched stats for device {device_id}"`: Successfully retrieved device statistics
- `"Failed to fetch stats for device {device_id}"`: Device statistics unavailable (not critical)
- `"Fetched X items across Y pages"`: Pagination working correctly

## Trust These Instructions

**These instructions have been validated** by:
- Running `ruff check` on the codebase (all checks passed)
- Running `ruff format --check` (all files formatted)
- Exploring all configuration files and source code
- Testing Ruff commands on sample files

**Only search/explore if:**
- Information here is incomplete for your specific task
- You encounter an error contradicting these instructions
- You need to understand implementation details not covered here

For most tasks, these instructions provide everything needed to make changes confidently without extensive exploration.
