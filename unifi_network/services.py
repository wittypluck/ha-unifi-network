"""UniFi Network services."""

from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, SERVICE_REMOVE_STALE_CLIENTS
from .core import UnifiNetworkCore

_LOGGER = logging.getLogger(__name__)


def _get_entries_to_process(
    hass: HomeAssistant, config_entry_id: str | None
) -> list[ConfigEntry]:
    """Get config entries to process for stale client removal."""
    entries_to_process = []

    if config_entry_id:
        # First try to find by ID (UUID format)
        if config_entry_id in hass.data.get(DOMAIN, {}):
            entry = hass.config_entries.async_get_entry(config_entry_id)
            if entry and entry.domain == DOMAIN:
                entries_to_process.append(entry)
            else:
                _LOGGER.error(
                    "Config entry %s not found or not a UniFi Network integration",
                    config_entry_id,
                )
        else:
            # Try to find by title/name
            all_entries = [
                entry
                for entry in hass.config_entries.async_entries(DOMAIN)
                if entry.entry_id in hass.data.get(DOMAIN, {})
            ]

            matching_entries = [
                entry for entry in all_entries if entry.title == config_entry_id
            ]

            if matching_entries:
                entries_to_process.extend(matching_entries)
                if len(matching_entries) > 1:
                    _LOGGER.warning(
                        "Multiple config entries found with title '%s', processing all %d entries",
                        config_entry_id,
                        len(matching_entries),
                    )
            else:
                _LOGGER.error(
                    "No config entry found with ID or title '%s'. Available entries: %s",
                    config_entry_id,
                    [entry.title for entry in all_entries],
                )
    else:
        # Process all UniFi Network config entries
        entries_to_process = [
            entry
            for entry in hass.config_entries.async_entries(DOMAIN)
            if entry.entry_id in hass.data.get(DOMAIN, {})
        ]

    return entries_to_process


def _process_entry_devices(
    hass: HomeAssistant,
    device_reg: dr.DeviceRegistry,
    entry: ConfigEntry,
    core: UnifiNetworkCore,
) -> tuple[int, int]:
    """Process devices for a single config entry and return (removed, total_processed)."""
    # Get current devices (infrastructure devices)
    current_devices = (
        core.device_coordinator.data
        if core.device_coordinator and core.device_coordinator.data
        else {}
    )

    # Get device IDs
    current_device_ids = {device.id for device in current_devices.values()}

    # Get known_clients data
    known_clients = (
        core.client_coordinator.known_clients
        if core.client_coordinator and core.client_coordinator.known_clients
        else {}
    )

    # Get client IDs
    known_clients_ids = {client.id for client in known_clients.values()}

    # Get all devices in the registry for this config entry
    devices = dr.async_entries_for_config_entry(device_reg, entry.entry_id)

    removed_count = 0
    total_processed = 0

    for device in devices:
        # Get device identifiers for this integration and convert all to strings
        device_identifiers = [
            str(identifier[1])
            for identifier in device.identifiers
            if identifier[0] == DOMAIN
        ]

        if not device_identifiers:
            continue

        total_processed += 1

        # Debug log for processed device
        _LOGGER.debug(
            "Processing device: %s (all identifiers: %s)",
            device.name or "Unknown",
            device.identifiers,
        )

        device_id = device_identifiers[0]  # Use the first identifier

        in_current_devices = device_id in current_device_ids
        in_known_clients = device_id in known_clients_ids

        # Check if this device should be kept - only check devices and known clients
        should_keep = in_current_devices or in_known_clients

        if should_keep:
            continue

        # This device is not in any of our known lists - it's stale
        _LOGGER.info(
            "Removing stale device: %s (ID: %s) from entry %s",
            device.name or "Unknown",
            device_id,
            entry.title,
        )
        device_reg.async_remove_device(device.id)
        removed_count += 1

    return removed_count, total_processed


async def async_remove_stale_clients(call: ServiceCall) -> None:
    """Remove stale clients from device registry."""
    hass = call.hass
    config_entry_id = call.data.get("config_entry_id")

    # Get device registry
    device_reg = dr.async_get(hass)

    # Get config entries to process
    entries_to_process = _get_entries_to_process(hass, config_entry_id)

    if not entries_to_process:
        _LOGGER.warning("No UniFi Network integrations found to process")
        return

    total_removed = 0
    total_processed = 0

    for entry in entries_to_process:
        core = hass.data[DOMAIN][entry.entry_id]
        removed_count, processed_count = _process_entry_devices(
            hass, device_reg, entry, core
        )
        total_removed += removed_count
        total_processed += processed_count

    _LOGGER.info(
        "Stale client cleanup completed: removed %d devices out of %d processed",
        total_removed,
        total_processed,
    )


def async_register_services(hass: HomeAssistant) -> None:
    """Register UniFi Network services."""
    if not hass.services.has_service(DOMAIN, SERVICE_REMOVE_STALE_CLIENTS):
        hass.services.async_register(
            DOMAIN,
            SERVICE_REMOVE_STALE_CLIENTS,
            async_remove_stale_clients,
            schema=vol.Schema(
                {
                    vol.Optional("config_entry_id"): str,
                }
            ),
        )


def async_unregister_services(hass: HomeAssistant) -> None:
    """Unregister UniFi Network services."""
    hass.services.async_remove(DOMAIN, SERVICE_REMOVE_STALE_CLIENTS)
