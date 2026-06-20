"""Tests for device tracker client attributes."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import Mock

from custom_components.unifi_network.device_tracker import UnifiClientTracker


class TestUnifiClientTracker:
    """Test client tracker attribute behavior."""

    def test_extra_state_attributes_with_resolved_uplink_device(self):
        """Expose resolved uplink MAC and name when lookup succeeds."""
        client_id = "client_123"
        now = datetime(2026, 1, 1, tzinfo=UTC)

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.last_seen = now
        client.uplink_device_id = "device_1"
        client.overview = Mock()
        client.overview.connected_at = "2026-01-01T00:00:00+00:00"

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        uplink_device = Mock()
        uplink_device.mac = "11:22:33:44:55:66"
        uplink_device.name = "Core Switch"

        device_coordinator = Mock()
        device_coordinator.get_device.return_value = uplink_device

        tracker = UnifiClientTracker(client_coordinator, client_id, device_coordinator)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert attrs["mac"] == "aa:bb:cc:dd:ee:ff"
        assert attrs["ip"] == "192.168.1.10"
        assert attrs["last_seen"] == now
        assert attrs["connected_at"] == "2026-01-01T00:00:00+00:00"
        assert attrs["uplink_mac"] == "11:22:33:44:55:66"
        assert attrs["uplink_device_name"] == "Core Switch"
        device_coordinator.get_device.assert_called_once_with("device_1")

    def test_extra_state_attributes_without_device_coordinator(self):
        """Keep uplink keys with None values when devices are disabled."""
        client_id = "client_123"

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.last_seen = None
        client.uplink_device_id = "device_1"
        client.overview = Mock()
        client.overview.connected_at = None

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert attrs["uplink_mac"] is None
        assert attrs["uplink_device_name"] is None

    def test_extra_state_attributes_with_unknown_uplink_device(self):
        """Keep uplink keys with None values when lookup misses."""
        client_id = "client_123"

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.last_seen = None
        client.uplink_device_id = "missing-device"
        client.overview = Mock()
        client.overview.connected_at = None

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        device_coordinator = Mock()
        device_coordinator.get_device.return_value = None

        tracker = UnifiClientTracker(client_coordinator, client_id, device_coordinator)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert attrs["uplink_mac"] is None
        assert attrs["uplink_device_name"] is None
        device_coordinator.get_device.assert_called_once_with("missing-device")

    def test_extra_state_attributes_with_missing_uplink_device_id(self):
        """Keep uplink keys with None values when client has no uplink ID."""
        client_id = "client_123"

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.last_seen = None
        client.uplink_device_id = None
        client.overview = Mock()
        client.overview.connected_at = None

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        device_coordinator = Mock()

        tracker = UnifiClientTracker(client_coordinator, client_id, device_coordinator)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert attrs["uplink_mac"] is None
        assert attrs["uplink_device_name"] is None
        device_coordinator.get_device.assert_not_called()

    def test_extra_state_attributes_returns_none_when_client_missing(self):
        """Return None attributes when coordinator cannot resolve client."""
        client_id = "client_123"

        client_coordinator = Mock()
        client_coordinator.data = {}
        client_coordinator.get_client.return_value = None

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        assert tracker.extra_state_attributes is None
