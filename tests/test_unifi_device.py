"""Tests for UnifiDevice wrapper functionality."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

# Import conftest to set up mocks
import tests.conftest  # noqa: F401
from unifi_network.api_client.types import Unset

# Remove unused imports - ATTR_MANUFACTURER, DOMAIN not needed in simplified tests
from unifi_network.unifi_device import UnifiDevice


class TestUnifiDevice:
    """Test the UnifiDevice wrapper class."""

    @pytest.fixture
    def basic_device_overview(self):
        """Create a basic device overview mock."""
        overview = Mock()
        overview.id = "device-123"
        overview.name = "Test Device"
        overview.ip_address = "192.168.1.10"
        overview.mac_address = "aa:bb:cc:dd:ee:ff"
        overview.model = "Test Model"
        return overview

    @pytest.fixture
    def device_with_unset_values(self):
        """Create a device overview with Unset values."""
        overview = Mock()
        overview.id = "device-456"
        overview.name = Unset()
        overview.ip_address = Unset()
        overview.mac_address = Unset()
        overview.model = "Test Model"
        return overview

    @pytest.fixture
    def device_statistics(self):
        """Create device statistics mock."""
        stats = Mock()
        stats.uptime = 12345
        stats.load_average_1 = 1.5
        stats.cpu_utilization = 25.5
        return stats

    @pytest.fixture
    def device_details(self):
        """Create device details mock."""
        details = Mock()
        details.firmware_version = "1.0.0"
        details.firmware_updatable = True
        return details

    @pytest.fixture
    def device_details_with_unset(self):
        """Create device details with Unset values."""
        details = Mock()
        details.firmware_version = Unset()
        details.firmware_updatable = False
        return details

    def test_basic_device_properties(
        self, basic_device_overview, device_statistics, device_details
    ):
        """Test basic device properties with valid data."""
        device = UnifiDevice(
            overview=basic_device_overview,
            latest_statistics=device_statistics,
            details=device_details,
        )

        assert device.id == "device-123"
        assert device.name == "Test Device"
        assert device.ip == "192.168.1.10"
        assert device.mac == "aa:bb:cc:dd:ee:ff"
        assert device.firmware_version == "1.0.0"
        assert device.firmware_updatable is True

    def test_device_with_unset_values(self, device_with_unset_values):
        """Test device properties when API returns Unset values."""
        device = UnifiDevice(
            overview=device_with_unset_values, latest_statistics=None, details=None
        )

        assert device.id == "device-456"
        assert device.name is None
        assert device.ip is None
        assert device.mac is None
        assert device.firmware_version is None
        assert device.firmware_updatable is False

    def test_device_with_missing_attributes(self):
        """Test device when getattr returns None for missing attributes."""
        overview = Mock()
        overview.id = "device-789"

        # Mock getattr behavior to return None for specific attributes
        def mock_getattr(obj, name, default=None):
            if name in ["name", "ip_address", "mac_address"]:
                return default
            return Mock()

        with patch("unifi_network.unifi_device.getattr", side_effect=mock_getattr):
            device = UnifiDevice(
                overview=overview, latest_statistics=None, details=None
            )

            assert device.id == "device-789"
            assert device.name is None
            assert device.ip is None
            assert device.mac is None

    def test_device_with_no_details(self, basic_device_overview):
        """Test device properties when details are None."""
        device = UnifiDevice(
            overview=basic_device_overview, latest_statistics=None, details=None
        )

        assert device.firmware_version is None
        assert device.firmware_updatable is False

    def test_device_with_unset_details(
        self, basic_device_overview, device_details_with_unset
    ):
        """Test device properties when details contain Unset values."""
        device = UnifiDevice(
            overview=basic_device_overview,
            latest_statistics=None,
            details=device_details_with_unset,
        )

        assert device.firmware_version is None
        assert device.firmware_updatable is False

    def test_device_info_with_complete_data(self, basic_device_overview):
        """Test device_info property with complete data."""
        device = UnifiDevice(
            overview=basic_device_overview, latest_statistics=None, details=None
        )

        device_info = device.device_info

        # DeviceInfo is mocked, so just verify it was created with the device
        assert device_info is not None

    def test_device_info_with_no_mac(self, device_with_unset_values):
        """Test device_info property when MAC address is not available."""
        device = UnifiDevice(
            overview=device_with_unset_values, latest_statistics=None, details=None
        )

        device_info = device.device_info

        # DeviceInfo is mocked, so just verify it was created
        assert device_info is not None

    def test_id_property_conversion(self):
        """Test that id property always returns a string."""
        overview = Mock()
        overview.id = 12345  # Integer ID

        device = UnifiDevice(overview=overview, latest_statistics=None, details=None)

        assert device.id == "12345"
        assert isinstance(device.id, str)

    def test_device_without_details_attribute(self, basic_device_overview):
        """Test device when details object is missing expected attributes."""
        details = Mock()

        # Mock getattr behavior to return None for firmware attributes
        def mock_getattr(obj, name, default=None):
            if name in ["firmware_version", "firmware_updatable"]:
                return default
            return Mock()

        with patch("unifi_network.unifi_device.getattr", side_effect=mock_getattr):
            device = UnifiDevice(
                overview=basic_device_overview, latest_statistics=None, details=details
            )

            assert device.firmware_version is None
            assert device.firmware_updatable is False
