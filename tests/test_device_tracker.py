"""Tests for device tracker client attributes."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from custom_components.unifi_network.api_client.types import UNSET
from custom_components.unifi_network.const import DOMAIN
from custom_components.unifi_network.device_tracker import (
    UnifiClientTracker,
    async_setup_entry,
)


class TestUnifiClientTracker:
    """Test client tracker attribute behavior."""

    def test_hostname_returns_client_name(self):
        """Expose client name via hostname property."""
        client_id = "client_123"

        client = Mock()
        client.name = "laptop-01"

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        assert tracker.hostname == "laptop-01"
        assert tracker.unique_id == "unifi_client_client_123_device_tracker"

    def test_hostname_returns_none_when_client_missing(self):
        """Return None hostname when coordinator cannot resolve client."""
        client_id = "client_123"

        client_coordinator = Mock()
        client_coordinator.data = {}
        client_coordinator.get_client.return_value = None

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        assert tracker.hostname is None
        assert tracker.unique_id == "unifi_client_client_123_device_tracker"

    def test_tracker_with_missing_mac_still_reports_connection_state(self):
        """Clients without a MAC should still be tracked via BaseScannerEntity."""
        client_id = "client_no_mac"

        client = Mock()
        client.mac = None
        client.ip = "192.168.1.55"
        client.name = "tablet-no-mac"

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        assert tracker.mac_address is None
        assert tracker.ip_address == "192.168.1.55"
        assert tracker.hostname == "tablet-no-mac"
        assert tracker.is_connected is True

    def test_tracker_with_missing_mac_reports_disconnected_when_client_removed(self):
        """No-MAC clients should become not connected when absent from data."""
        client_id = "client_no_mac"

        client = Mock()
        client.mac = None
        client.ip = "192.168.1.55"
        client.name = "tablet-no-mac"

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)
        assert tracker.is_connected is True

        client_coordinator.data = {}
        assert tracker.is_connected is False

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
        assert attrs["last_seen"] == now
        assert attrs["connected_at"] == "2026-01-01T00:00:00+00:00"
        assert attrs["uplink_mac"] == "11:22:33:44:55:66"
        assert attrs["uplink_device_name"] == "Core Switch"
        device_coordinator.get_device.assert_called_once_with("device_1")

    def test_extra_state_attributes_exposes_base_client_fields(self):
        """Expose client identity fields in tracker attributes."""
        client_id = "client_123"

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.name = "laptop-01"
        client.last_seen = None
        client.uplink_device_id = None
        client.overview = Mock()
        client.overview.connected_at = None

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert attrs["mac"] == "aa:bb:cc:dd:ee:ff"
        assert attrs["ip"] == "192.168.1.10"
        assert attrs["hostname"] == "laptop-01"
        assert attrs["last_seen"] is None

    def test_extra_state_attributes_omits_connected_at_when_unset(self):
        """Do not include connected_at when API returns UNSET."""
        client_id = "client_123"

        client = Mock()
        client.mac = "aa:bb:cc:dd:ee:ff"
        client.ip = "192.168.1.10"
        client.name = "laptop-01"
        client.last_seen = None
        client.uplink_device_id = None
        client.overview = Mock()
        client.overview.connected_at = UNSET

        client_coordinator = Mock()
        client_coordinator.data = {client_id: client}
        client_coordinator.get_client.return_value = client

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        attrs = tracker.extra_state_attributes

        assert attrs is not None
        assert "connected_at" not in attrs

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


@pytest.mark.asyncio
async def test_async_setup_entry_adds_clients_and_listener():
    """Create initial tracker entities and register a listener."""
    entry_id = "entry-1"
    client_id = "client-1"

    coordinator = Mock()
    coordinator.data = {client_id: Mock()}
    coordinator.async_add_listener = Mock()

    core = Mock()
    core.client_coordinator = coordinator
    core.device_coordinator = None

    hass = Mock()
    hass.data = {DOMAIN: {entry_id: core}}

    entry = Mock()
    entry.entry_id = entry_id

    added_entities: list[UnifiClientTracker] = []

    def _async_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_entry(hass, entry, _async_add_entities)
    coordinator.async_add_listener.assert_called_once()
    assert len(added_entities) == 1
    assert isinstance(added_entities[0], UnifiClientTracker)
