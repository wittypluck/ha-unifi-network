"""Tests for the UnifiClient class."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from custom_components.unifi_network.api_client.types import Unset
from custom_components.unifi_network.unifi_client import UnifiClient


class TestUnifiClient:
    """Test the UnifiClient class."""

    def test_client_id_property(self):
        """Test that client ID is returned as string."""
        mock_overview = MagicMock()
        mock_overview.id = 12345

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.id == "12345"

    def test_client_name_property_with_value(self):
        """Test client name property when name is present."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.name = "My iPhone"

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.name == "My iPhone"

    def test_client_name_property_with_unset(self):
        """Test client name property when name is Unset (missing)."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.name = Unset()

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.name is None

    def test_client_name_property_with_missing_attribute(self):
        """Test client name property when name attribute is missing."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        # Don't set name attribute - it will be missing
        del mock_overview.name

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.name is None

    def test_client_ip_property_with_value(self):
        """Test client IP property when IP address is present."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.ip_address = "192.168.1.100"

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.ip == "192.168.1.100"

    def test_client_ip_property_with_unset(self):
        """Test client IP property when IP address is Unset (missing)."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.ip_address = Unset()

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.ip is None

    def test_client_ip_property_with_missing_attribute(self):
        """Test client IP property when ip_address attribute is missing."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        # Don't set ip_address attribute
        del mock_overview.ip_address

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.ip is None

    def test_client_mac_property_from_overview(self):
        """Test MAC address property from overview additional_properties."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.additional_properties = {"macAddress": "aa:bb:cc:dd:ee:ff"}

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.mac == "aa:bb:cc:dd:ee:ff"

    def test_client_mac_property_from_details(self):
        """Test MAC address property from details additional_properties."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.additional_properties = {}

        mock_details = MagicMock()
        mock_details.additional_properties = {"macAddress": "11:22:33:44:55:66"}

        client = UnifiClient(overview=mock_overview, details=mock_details)

        assert client.mac == "11:22:33:44:55:66"

    def test_client_mac_property_with_unset(self):
        """Test MAC address property when MAC is Unset."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.additional_properties = {"macAddress": Unset()}

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.mac is None

    def test_client_mac_property_with_no_additional_properties(self):
        """Test MAC address property when no additional_properties exist."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        # No additional_properties attribute
        del mock_overview.additional_properties

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.mac is None

    def test_client_mac_property_with_empty_mac(self):
        """Test MAC address property when MAC is empty string."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.additional_properties = {"macAddress": ""}

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.mac is None

    def test_device_info_with_complete_data(self):
        """Test DeviceInfo generation with complete client data."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.name = "My Device"
        mock_overview.type_ = "smartphone"
        mock_overview.additional_properties = {"macAddress": "aa:bb:cc:dd:ee:ff"}

        client = UnifiClient(overview=mock_overview, details=None)
        client.vendor = "Apple"  # Set vendor manually for testing

        # Should not raise exception when creating DeviceInfo
        device_info = client.device_info
        assert device_info is not None

    def test_device_info_with_missing_data(self):
        """Test DeviceInfo generation with missing client data."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.name = Unset()
        mock_overview.type_ = Unset()
        mock_overview.additional_properties = {}

        client = UnifiClient(overview=mock_overview, details=None)

        # Should not raise exception when creating DeviceInfo with missing data
        device_info = client.device_info
        assert device_info is not None

    def test_update_method_with_valid_client(self):
        """Test updating client with another UnifiClient instance."""
        # Original client
        mock_overview1 = MagicMock()
        mock_overview1.id = "client_123"
        mock_overview1.name = "Old Name"

        mock_details1 = MagicMock()
        old_time = datetime(2023, 1, 1, tzinfo=UTC)

        client = UnifiClient(
            overview=mock_overview1, details=mock_details1, last_seen=old_time
        )

        # Updated client
        mock_overview2 = MagicMock()
        mock_overview2.id = "client_123"
        mock_overview2.name = "New Name"

        mock_details2 = MagicMock()
        new_time = datetime(2023, 12, 31, tzinfo=UTC)

        other_client = UnifiClient(
            overview=mock_overview2, details=mock_details2, last_seen=new_time
        )

        # Update original client
        client.update(other_client)

        # Verify update
        assert client.overview == mock_overview2
        assert client.details == mock_details2
        assert client.last_seen == new_time
        assert client.name == "New Name"

    def test_update_method_with_invalid_type(self):
        """Test updating client with non-UnifiClient object raises TypeError."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"

        client = UnifiClient(overview=mock_overview, details=None)

        # Try to update with wrong type
        with pytest.raises(
            TypeError, match="Can only update from another UnifiClient instance"
        ):
            client.update("not a client")

    def test_last_seen_property(self):
        """Test last_seen property is properly stored and retrieved."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"

        last_seen_time = datetime(2023, 6, 15, 10, 30, 0, tzinfo=UTC)

        client = UnifiClient(
            overview=mock_overview, details=None, last_seen=last_seen_time
        )

        assert client.last_seen == last_seen_time

    def test_client_with_none_details(self):
        """Test client works correctly when details is None."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.name = "Test Client"
        mock_overview.additional_properties = {"macAddress": "aa:bb:cc:dd:ee:ff"}

        client = UnifiClient(overview=mock_overview, details=None)

        assert client.id == "client_123"
        assert client.name == "Test Client"
        assert client.mac == "aa:bb:cc:dd:ee:ff"
        assert client.details is None

    def test_mac_priority_overview_over_details(self):
        """Test that MAC from overview takes priority over details."""
        mock_overview = MagicMock()
        mock_overview.id = "client_123"
        mock_overview.additional_properties = {"macAddress": "overview:mac:addr"}

        mock_details = MagicMock()
        mock_details.additional_properties = {"macAddress": "details:mac:addr"}

        client = UnifiClient(overview=mock_overview, details=mock_details)

        # Should prefer overview MAC
        assert client.mac == "overview:mac:addr"
