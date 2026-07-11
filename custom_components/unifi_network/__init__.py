from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, PLATFORMS
from .core import UnifiNetworkCore
from .services import async_register_services, async_unregister_services

_LOGGER = logging.getLogger(__name__)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old config entries and related entity registry records."""
    _LOGGER.info(
        "Check migration config entry %s from version %s", entry.entry_id, entry.version
    )
    if entry.version != 1:
        return True

    _LOGGER.info(
        "Migrating config entry %s from version %s", entry.entry_id, entry.version
    )

    ent_reg = er.async_get(hass)
    registry_entries = er.async_entries_for_config_entry(ent_reg, entry.entry_id)

    for reg_entry in registry_entries:
        _LOGGER.info(
            "Considering entry %s entity_id %s",
            reg_entry.unique_id,
            reg_entry.entity_id,
        )

        if reg_entry.config_entry_id != entry.entry_id:
            _LOGGER.info("1")
            continue
        if not reg_entry.entity_id.startswith("device_tracker."):
            _LOGGER.info("2")
            continue
        if not reg_entry.entity_id.endswith("_2"):
            _LOGGER.info("3")
            continue
        _LOGGER.info(
            "Looking for old entry for entry %s entity_id %s",
            reg_entry.unique_id,
            reg_entry.entity_id,
        )

        base_entity_id = reg_entry.entity_id[:-2]
        old_entry = ent_reg.async_get(base_entity_id)
        if old_entry and old_entry.config_entry_id == entry.entry_id:
            _LOGGER.info(
                "Found old entry %s entity_id %s",
                old_entry.unique_id,
                old_entry.entity_id,
            )

            ent_reg.async_remove(base_entity_id)
            ent_reg.async_update_entity(
                reg_entry.entity_id, new_entity_id=base_entity_id
            )

    hass.config_entries.async_update_entry(entry, version=2)
    _LOGGER.info("Migration to version 2 successful for entry %s", entry.entry_id)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the integration."""
    core = UnifiNetworkCore(
        hass,
        base_url=entry.data["base_url"],
        site_id=entry.data["site_id"],
        api_key=entry.data.get("api_key"),
        enable_devices=entry.data.get("enable_devices", True),
        enable_clients=entry.data.get("enable_clients", True),
        verify_ssl=entry.data.get("verify_ssl", True),
        devices_filter=entry.options.get("devices_filter"),
        clients_filter=entry.options.get("clients_filter"),
    )
    await core.async_init()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = core
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services (only once, not per config entry)
    async_register_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

        # Remove service if this is the last config entry
        if not hass.data[DOMAIN]:
            async_unregister_services(hass)

    return unload_ok


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Remove config entry from a device."""
    core = hass.data[DOMAIN][config_entry.entry_id]

    devices = (
        core.device_coordinator.data
        if core.device_coordinator and core.device_coordinator.data
        else {}
    )
    clients = (
        core.client_coordinator.data
        if core.client_coordinator and core.client_coordinator.data
        else {}
    )

    return not any(
        identifier
        for identifier in device_entry.identifiers
        if identifier[0] == DOMAIN
        and (identifier[1] in devices or identifier[1] in clients)
    )
