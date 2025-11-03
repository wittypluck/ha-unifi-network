from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, PLATFORMS
from .core import UnifiNetworkCore


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
    )
    await core.async_init()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = core
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
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
