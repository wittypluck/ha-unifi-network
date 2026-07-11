"""Tests for integration setup and config entry migration."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from custom_components.unifi_network import async_migrate_entry
from custom_components.unifi_network.const import DOMAIN

TRACKER_UNIQUE_ID = "20:df:b9:9c:fb:e6"


@pytest.mark.asyncio
async def test_async_migrate_entry_renames_duplicate_tracker_entity():
    """Migrate duplicate tracker ids even when unique_id format changed."""
    hass = Mock()
    hass.config_entries = Mock()

    entry = Mock()
    entry.entry_id = "entry-1"
    entry.version = 1

    duplicate_entry = Mock()
    duplicate_entry.entity_id = "device_tracker.unifi_client_client_1_2"
    duplicate_entry.platform = DOMAIN
    duplicate_entry.config_entry_id = entry.entry_id
    duplicate_entry.unique_id = TRACKER_UNIQUE_ID

    old_entry = Mock()
    old_entry.config_entry_id = entry.entry_id
    old_entry.platform = DOMAIN
    old_entry.unique_id = "legacy-unique-id"

    entity_registry = Mock()
    entity_registry.async_get.side_effect = lambda entity_id: (
        old_entry if entity_id == "device_tracker.unifi_client_client_1" else None
    )

    with (
        patch(
            "custom_components.unifi_network.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.er.async_entries_for_config_entry",
            return_value=[duplicate_entry],
        ),
    ):
        result = await async_migrate_entry(hass, entry)

    assert result is True
    entity_registry.async_remove.assert_called_once_with(
        "device_tracker.unifi_client_client_1"
    )
    entity_registry.async_update_entity.assert_called_once_with(
        "device_tracker.unifi_client_client_1_2",
        new_entity_id="device_tracker.unifi_client_client_1",
    )
    hass.config_entries.async_update_entry.assert_called_once_with(entry, version=2)


@pytest.mark.asyncio
async def test_async_migrate_entry_skips_invalid_candidates():
    """Skip migration for wrong entity domain, wrong entry, or mismatched ids."""
    hass = Mock()
    hass.config_entries = Mock()

    entry = Mock()
    entry.entry_id = "entry-1"
    entry.version = 1

    wrong_platform = Mock()
    wrong_platform.entity_id = "sensor.unifi_client_client_1_2"
    wrong_platform.platform = DOMAIN
    wrong_platform.config_entry_id = entry.entry_id
    wrong_platform.unique_id = TRACKER_UNIQUE_ID

    wrong_config_entry = Mock()
    wrong_config_entry.entity_id = "device_tracker.unifi_client_client_1_2"
    wrong_config_entry.platform = DOMAIN
    wrong_config_entry.config_entry_id = "other-entry"
    wrong_config_entry.unique_id = TRACKER_UNIQUE_ID

    wrong_entity_domain = Mock()
    wrong_entity_domain.entity_id = "sensor.google_home_mini_a_2"
    wrong_entity_domain.platform = DOMAIN
    wrong_entity_domain.config_entry_id = entry.entry_id
    wrong_entity_domain.unique_id = TRACKER_UNIQUE_ID

    missing_base_entry = Mock()
    missing_base_entry.entity_id = "device_tracker.nonexistent_2"
    missing_base_entry.platform = DOMAIN
    missing_base_entry.config_entry_id = entry.entry_id
    missing_base_entry.unique_id = TRACKER_UNIQUE_ID

    old_entry = Mock()
    old_entry.config_entry_id = entry.entry_id
    old_entry.platform = DOMAIN
    old_entry.unique_id = "ac:67:84:24:e4:b7"

    entity_registry = Mock()
    entity_registry.async_get.side_effect = lambda entity_id: (
        old_entry if entity_id == "device_tracker.unifi_client_client_1" else None
    )

    with (
        patch(
            "custom_components.unifi_network.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.er.async_entries_for_config_entry",
            return_value=[
                wrong_platform,
                wrong_config_entry,
                wrong_entity_domain,
                missing_base_entry,
            ],
        ),
    ):
        result = await async_migrate_entry(hass, entry)

    assert result is True
    entity_registry.async_remove.assert_not_called()
    entity_registry.async_update_entity.assert_not_called()
    hass.config_entries.async_update_entry.assert_called_once_with(entry, version=2)


@pytest.mark.asyncio
async def test_async_migrate_entry_migrates_when_unique_ids_differ():
    """Migrate based on entity_id collision when unique_ids are different."""
    hass = Mock()
    hass.config_entries = Mock()

    entry = Mock()
    entry.entry_id = "entry-1"
    entry.version = 1

    duplicate_entry = Mock()
    duplicate_entry.entity_id = "device_tracker.starlight_2"
    duplicate_entry.platform = DOMAIN
    duplicate_entry.config_entry_id = entry.entry_id
    duplicate_entry.unique_id = "80:ee:73:cb:33:98"

    old_entry = Mock()
    old_entry.entity_id = "device_tracker.starlight"
    old_entry.config_entry_id = entry.entry_id
    old_entry.platform = DOMAIN
    old_entry.unique_id = "legacy-unique-id"

    entity_registry = Mock()
    entity_registry.async_get.side_effect = lambda entity_id: (
        old_entry if entity_id == "device_tracker.starlight" else None
    )

    with (
        patch(
            "custom_components.unifi_network.er.async_get",
            return_value=entity_registry,
        ),
        patch(
            "custom_components.unifi_network.er.async_entries_for_config_entry",
            return_value=[duplicate_entry],
        ),
    ):
        result = await async_migrate_entry(hass, entry)

    assert result is True
    entity_registry.async_remove.assert_called_once_with("device_tracker.starlight")
    entity_registry.async_update_entity.assert_called_once_with(
        "device_tracker.starlight_2",
        new_entity_id="device_tracker.starlight",
    )
    hass.config_entries.async_update_entry.assert_called_once_with(entry, version=2)


@pytest.mark.asyncio
async def test_async_migrate_entry_skips_when_version_is_current():
    """Do nothing when the config entry is already on the current version."""
    hass = Mock()
    hass.config_entries = Mock()

    entry = Mock()
    entry.entry_id = "entry-1"
    entry.version = 2

    with patch("custom_components.unifi_network.er.async_get") as async_get:
        result = await async_migrate_entry(hass, entry)

    assert result is True
    async_get.assert_not_called()
    hass.config_entries.async_update_entry.assert_not_called()
