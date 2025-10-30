from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

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
