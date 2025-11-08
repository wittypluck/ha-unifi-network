"""Tests for coordinator functionality."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

# Import conftest to set up mocks
import tests.conftest

# Now import the modules after mocks are set up
from unifi_network.coordinator import UnifiClientCoordinator, UnifiDeviceCoordinator


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    return tests.conftest.MockHomeAssistant()


@pytest.fixture
def mock_api_client():
    """Create a mock API client."""
    return Mock()


@pytest.fixture
def device_coordinator(mock_hass, mock_api_client):
    """Create a device coordinator instance."""
    return UnifiDeviceCoordinator(mock_hass, mock_api_client, "test-site")


@pytest.fixture
def client_coordinator(mock_hass, mock_api_client):
    """Create a client coordinator instance."""
    return UnifiClientCoordinator(mock_hass, mock_api_client, "test-site")


@pytest.fixture
def mock_device_overview():
    """Mock device overview."""
    device = Mock()
    device.id = "device-123"
    device.name = "Test Device"
    device.ip_address = "192.168.1.10"
    device.mac_address = "aa:bb:cc:dd:ee:ff"
    device.model = "Test Model"
    return device


@pytest.fixture
def mock_device_statistics():
    """Mock device statistics."""
    stats = Mock()
    stats.uptime = 12345
    stats.load_average_1 = 1.5
    stats.load_average_5 = 2.0
    stats.load_average_15 = 1.8
    stats.cpu_utilization = 25.5
    stats.memory_utilization = 45.0
    return stats


@pytest.fixture
def mock_device_details():
    """Mock device details."""
    details = Mock()
    details.firmware_version = "1.0.0"
    details.firmware_updatable = True
    return details


@pytest.fixture
def mock_client_overview():
    """Mock client overview."""
    client = Mock()
    client.id = "client-456"
    client.name = "Test Client"
    client.ip_address = "192.168.1.20"
    client.mac_address = "ff:ee:dd:cc:bb:aa"
    return client


@pytest.fixture
def mock_client_details():
    """Mock client details."""
    details = Mock()
    details.connected_at = "2023-01-01T12:00:00Z"
    details.connection_state = "Connected"
    return details


class TestUnifiDeviceCoordinator:
    """Test the UniFi Device coordinator."""

    async def test_fetch_devices_success(
        self,
        device_coordinator,
        mock_device_overview,
        mock_device_statistics,
        mock_device_details,
    ):
        """Test successful device fetching."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_device_overview],
            ),
            patch(
                "unifi_network.coordinator.get_device_latest_statistics.asyncio",
                return_value=mock_device_statistics,
            ),
            patch(
                "unifi_network.coordinator.get_device_details.asyncio",
                return_value=mock_device_details,
            ),
        ):
            result = await device_coordinator._fetch_and_merge()

        assert len(result) == 1
        assert "device-123" in result
        device = result["device-123"]
        assert device.overview == mock_device_overview
        assert device.latest_statistics == mock_device_statistics
        assert device.details == mock_device_details

    async def test_fetch_devices_with_missing_id(self, device_coordinator):
        """Test device fetching when device has no ID."""
        mock_device = Mock()
        mock_device.id = None

        with patch(
            "unifi_network.coordinator.fetch_all_pages",
            return_value=[mock_device],
        ):
            result = await device_coordinator._fetch_and_merge()

        assert len(result) == 0

    async def test_fetch_devices_with_statistics_failure(
        self, device_coordinator, mock_device_overview, mock_device_details
    ):
        """Test device fetching when statistics call fails."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_device_overview],
            ),
            patch(
                "unifi_network.coordinator.get_device_latest_statistics.asyncio",
                side_effect=Exception("Statistics failed"),
            ),
            patch(
                "unifi_network.coordinator.get_device_details.asyncio",
                return_value=mock_device_details,
            ),
        ):
            result = await device_coordinator._fetch_and_merge()

        assert len(result) == 1
        device = result["device-123"]
        assert device.overview == mock_device_overview
        assert device.latest_statistics is None
        assert device.details == mock_device_details

    async def test_fetch_devices_with_details_failure(
        self, device_coordinator, mock_device_overview, mock_device_statistics
    ):
        """Test device fetching when details call fails."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_device_overview],
            ),
            patch(
                "unifi_network.coordinator.get_device_latest_statistics.asyncio",
                return_value=mock_device_statistics,
            ),
            patch(
                "unifi_network.coordinator.get_device_details.asyncio",
                side_effect=Exception("Details failed"),
            ),
        ):
            result = await device_coordinator._fetch_and_merge()

        assert len(result) == 1
        device = result["device-123"]
        assert device.overview == mock_device_overview
        assert device.latest_statistics == mock_device_statistics
        assert device.details is None

    async def test_fetch_devices_api_failure(self, device_coordinator):
        """Test device fetching when main API call fails."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                side_effect=Exception("API failed"),
            ),
            pytest.raises(tests.conftest.UpdateFailed),
        ):
            await device_coordinator._fetch_and_merge()

    def test_get_device_existing(self, device_coordinator, mock_device_overview):
        """Test getting an existing device."""
        # Set up coordinator with data
        device_coordinator.data = {"device-123": Mock(overview=mock_device_overview)}

        result = device_coordinator.get_device("device-123")
        assert result is not None
        assert result.overview == mock_device_overview

    def test_get_device_nonexistent(self, device_coordinator):
        """Test getting a non-existent device."""
        device_coordinator.data = {}

        result = device_coordinator.get_device("nonexistent")
        assert result is None

    def test_get_device_no_data(self, device_coordinator):
        """Test getting device when coordinator has no data."""
        device_coordinator.data = None

        result = device_coordinator.get_device("device-123")
        assert result is None


class TestUnifiClientCoordinator:
    """Test the UniFi Client coordinator."""

    async def test_fetch_clients_success(
        self, client_coordinator, mock_client_overview, mock_client_details
    ):
        """Test successful client fetching."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_client_overview],
            ),
            patch(
                "unifi_network.coordinator.get_connected_client_details.asyncio",
                return_value=mock_client_details,
            ),
        ):
            result = await client_coordinator._fetch_and_merge()

        assert len(result) == 1
        assert "client-456" in result
        client = result["client-456"]
        assert client.overview == mock_client_overview
        assert client.details == mock_client_details
        assert client.last_seen is not None

    async def test_fetch_clients_with_missing_id(self, client_coordinator):
        """Test client fetching when client has no ID."""
        mock_client = Mock()
        mock_client.id = None

        with patch(
            "unifi_network.coordinator.fetch_all_pages",
            return_value=[mock_client],
        ):
            result = await client_coordinator._fetch_and_merge()

        assert len(result) == 0

    async def test_fetch_clients_with_details_failure(
        self, client_coordinator, mock_client_overview
    ):
        """Test client fetching when details call fails."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_client_overview],
            ),
            patch(
                "unifi_network.coordinator.get_connected_client_details.asyncio",
                side_effect=Exception("Details failed"),
            ),
        ):
            result = await client_coordinator._fetch_and_merge()

        assert len(result) == 1
        client = result["client-456"]
        assert client.overview == mock_client_overview
        assert client.details is None

    async def test_fetch_clients_api_failure(self, client_coordinator):
        """Test client fetching when main API call fails."""
        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                side_effect=Exception("API failed"),
            ),
            pytest.raises(tests.conftest.UpdateFailed),
        ):
            await client_coordinator._fetch_and_merge()

    async def test_fetch_clients_updates_known_clients(
        self, client_coordinator, mock_client_overview, mock_client_details
    ):
        """Test that known_clients are updated."""
        # Pre-populate known_clients
        existing_client = Mock()
        existing_client.id = "client-456"
        client_coordinator.known_clients = {"client-456": existing_client}

        with (
            patch(
                "unifi_network.coordinator.fetch_all_pages",
                return_value=[mock_client_overview],
            ),
            patch(
                "unifi_network.coordinator.get_connected_client_details.asyncio",
                return_value=mock_client_details,
            ),
        ):
            result = await client_coordinator._fetch_and_merge()

        assert len(result) == 1
        assert "client-456" in client_coordinator.known_clients
        # Verify update method was called
        existing_client.update.assert_called_once()

    def test_get_client_existing(self, client_coordinator, mock_client_overview):
        """Test getting an existing client."""
        # Set up coordinator with known clients
        client_coordinator.known_clients = {
            "client-456": Mock(overview=mock_client_overview)
        }

        result = client_coordinator.get_client("client-456")
        assert result is not None
        assert result.overview == mock_client_overview

    def test_get_client_nonexistent(self, client_coordinator):
        """Test getting a non-existent client."""
        client_coordinator.known_clients = {}

        result = client_coordinator.get_client("nonexistent")
        assert result is None
