# UniFi Network Integration Tests

This directory contains tests for the UniFi Network Home Assistant integration that **do not depend on Home Assistant core**. The tests validate key functionality and error handling scenarios without requiring the full Home Assistant environment.

## Test Coverage

The test suite validates the following requirements as requested:

### ✅ No exception if API calls fail
- `test_api_helpers.py::TestFetchAllPages::test_http_error_response`
- `test_api_helpers.py::TestFetchAllPages::test_none_response`  
- `test_api_helpers.py::TestFetchAllPages::test_no_parsed_response`
- `test_coordinator.py::TestUnifiDeviceCoordinator::test_fetch_devices_api_failure`
- `test_coordinator.py::TestUnifiClientCoordinator::test_fetch_clients_api_failure`

Tests that API failures are handled gracefully:
- HTTP error responses (500, 404, etc.)
- Network connectivity issues  
- Malformed/missing response data
- Individual device/client API call failures
- Coordinator-level error handling

### ✅ No exception if missing information in API responses
- `test_api_helpers.py::TestFetchAllPages::test_missing_data_attribute`
- `test_unifi_device.py::TestUnifiDevice::test_device_with_unset_values`
- `test_unifi_device.py::TestUnifiDevice::test_device_with_missing_attributes`
- `test_unifi_device.py::TestUnifiDevice::test_device_with_no_details`
- `test_coordinator.py::TestUnifiDeviceCoordinator::test_fetch_devices_with_statistics_failure`
- `test_coordinator.py::TestUnifiDeviceCoordinator::test_fetch_devices_with_details_failure`

Tests handling of:
- `Unset` values from the API client
- Missing optional device/client attributes
- Partial data when some API calls fail
- Pagination responses without data
- Device details/statistics unavailable

## Test Structure

### Core Test Files

- **`test_api_helpers.py`** - Tests for API helper functions (pagination, error handling)
- **`test_unifi_device.py`** - Tests for UnifiDevice wrapper (handling missing data)
- **`test_coordinator.py`** - Tests for data coordinators (API failure scenarios)

### Support Files

- **`conftest.py`** - Mock Home Assistant components to avoid dependencies
- **`pytest.ini`** - Pytest configuration for async test support

## Running Tests

### Prerequisites

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install ruff pytest pytest-asyncio attrs aiohttp voluptuous httpx python-dateutil
```

### Run All Tests

```bash
cd /path/to/ha-unifi-network
python -m pytest tests/ -v --asyncio-mode=auto
```

### Run Specific Test Categories

```bash
# API and data handling tests
python -m pytest tests/test_api_helpers.py tests/test_unifi_device.py -v --asyncio-mode=auto

# Coordinator error handling tests
python -m pytest tests/test_coordinator.py -v --asyncio-mode=auto
```

## Test Results Summary

✅ **53 tests passing** across 4 test files

- `test_api_helpers.py`: 10 tests (pagination, HTTP errors, malformed responses)
- `test_coordinator.py`: 15 tests (API failures, partial data, error propagation)
- `test_unifi_device.py`: 9 tests (Unset values, missing attributes, device info)
- `test_unifi_client.py`: 19 tests (client properties, MAC prioritization, DeviceInfo generation)

## Key Validated Scenarios

1. **Single Feature Selection**: Users can select devices-only or clients-only without exceptions
2. **API Resilience**: All API failure modes are handled gracefully without crashing
3. **Missing Data Handling**: Integration handles incomplete API responses robustly
4. **Error Propagation**: Errors are properly caught and logged, not leaked to users
5. **Pagination**: Large datasets are fetched correctly even with API inconsistencies

The tests demonstrate that the integration is robust against real-world API issues and configuration scenarios without requiring a full Home Assistant installation.
