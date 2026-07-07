"""Tests for device tracker client attributes."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import Mock, patch

import pytest

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

    def test_hostname_returns_none_when_client_missing(self):
        """Return None hostname when coordinator cannot resolve client."""
        client_id = "client_123"

        client_coordinator = Mock()
        client_coordinator.data = {}
        client_coordinator.get_client.return_value = None

        tracker = UnifiClientTracker(client_coordinator, client_id, None)

        assert tracker.hostname is None

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
async def test_async_setup_entry_migrates_duplicate_suffix_entity_id():
    """Remove old orphaned entry and rename '_2' entity to base entity_id."""
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

    duplicate_entry = Mock()
    duplicate_entry.entity_id = "device_tracker.unifi_client_client_1_2"
    duplicate_entry.platform = "device_tracker"
    duplicate_entry.config_entry_id = entry_id

    old_entry = Mock()
    old_entry.config_entry_id = entry_id

    entity_registry = Mock()
    entity_registry.async_get.side_effect = lambda entity_id: (
        old_entry if entity_id == "device_tracker.unifi_client_client_1" else None
    )

    added_entities: list[UnifiClientTracker] = []

    def _async_add_entities(entities):
        added_entities.extend(entities)

    with (
        patch(
            "custom_components.unifi_network.device_tracker.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.device_tracker.er.async_entries_for_config_entry",
            return_value=[duplicate_entry],
        ),
    ):
        await async_setup_entry(hass, entry, _async_add_entities)

    entity_registry.async_remove.assert_called_once_with(
        "device_tracker.unifi_client_client_1"
    )
    entity_registry.async_update_entity.assert_called_once_with(
        "device_tracker.unifi_client_client_1_2",
        new_entity_id="device_tracker.unifi_client_client_1",
    )
    coordinator.async_add_listener.assert_called_once()
    assert len(added_entities) == 1
    assert isinstance(added_entities[0], UnifiClientTracker)


@pytest.mark.asyncio
async def test_async_setup_entry_skips_migration_when_old_entry_is_not_from_config_entry():
    """Do not remove/rename when base entity belongs to a different config entry."""
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

    duplicate_entry = Mock()
    duplicate_entry.entity_id = "device_tracker.unifi_client_client_1_2"
    duplicate_entry.platform = "device_tracker"
    duplicate_entry.config_entry_id = entry_id

    old_entry = Mock()
    old_entry.config_entry_id = "different-entry"

    entity_registry = Mock()
    entity_registry.async_get.side_effect = lambda entity_id: (
        old_entry if entity_id == "device_tracker.unifi_client_client_1" else None
    )

    with (
        patch(
            "custom_components.unifi_network.device_tracker.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.device_tracker.er.async_entries_for_config_entry",
            return_value=[duplicate_entry],
        ),
    ):
        await async_setup_entry(hass, entry, Mock())

    entity_registry.async_remove.assert_not_called()
    entity_registry.async_update_entity.assert_not_called()


@pytest.mark.asyncio
async def test_async_setup_entry_skips_non_device_tracker_entries():
    """Skip migration candidates not from this config entry or non-device_tracker."""
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

    wrong_platform = Mock()
    wrong_platform.entity_id = "sensor.unifi_client_client_1_2"
    wrong_platform.platform = "sensor"
    wrong_platform.config_entry_id = entry_id

    wrong_config_entry = Mock()
    wrong_config_entry.entity_id = "device_tracker.unifi_client_client_1_2"
    wrong_config_entry.platform = "device_tracker"
    wrong_config_entry.config_entry_id = "other-entry"
    wrong_platform.config_entry_id = entry_id

    entity_registry = Mock()

    with (
        patch(
            "custom_components.unifi_network.device_tracker.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.device_tracker.er.async_entries_for_config_entry",
            return_value=[wrong_platform, wrong_config_entry],
        ),
    ):
        await async_setup_entry(hass, entry, Mock())

    entity_registry.async_get.assert_not_called()
    entity_registry.async_remove.assert_not_called()
    entity_registry.async_update_entity.assert_not_called()
