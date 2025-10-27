"""Unifi Network core module."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
# UpdateFailed is not required here; coordinators handle update errors

from .api_client import Client
from .coordinator import UnifiDeviceCoordinator


class UnifiNetworkCore:
    """Core class for Unifi Network integration."""

    def __init__(
        self, hass: HomeAssistant, base_url: str, site_id: str, api_key: str | None = None
    ) -> None:
        """Initialize Unifi Network core."""
        self.hass = hass
        self.site_id = site_id
        
        # Initialize API client
        headers = {"X-API-Key": api_key} if api_key else None
        self.client = Client(base_url=base_url, headers=headers)
        
        # Initialize coordinators
        self.device_coordinator = UnifiDeviceCoordinator(
            hass=hass,
            client=self.client,
            site_id=site_id,
        )
            
    async def async_init(self) -> None:
        """Initialize data and start updates."""
        await self.device_coordinator.async_config_entry_first_refresh()