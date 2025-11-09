"""Unifi Network core module."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import create_async_httpx_client

from .api_client import Client
from .coordinator import UnifiClientCoordinator, UnifiDeviceCoordinator


class UnifiNetworkCore:
    """Core class for Unifi Network integration."""

    def __init__(
        self,
        hass: HomeAssistant,
        base_url: str,
        site_id: str,
        api_key: str | None = None,
        enable_devices: bool = True,
        enable_clients: bool = True,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize Unifi Network core."""
        self.hass = hass
        self.site_id = site_id

        # Create httpx client using Home Assistant helper to avoid SSL blocking
        async_httpx_client = create_async_httpx_client(
            hass,
            verify_ssl=verify_ssl,
            base_url=base_url,
        )

        # Add API headers to the client
        if api_key:
            async_httpx_client.headers.update({"X-API-Key": api_key})

        # Initialize API client and set httpx client
        self.client = Client(base_url=base_url)
        self.client.set_async_httpx_client(async_httpx_client)

        # Initialize coordinators based on enabled features
        self.device_coordinator = None
        self.client_coordinator = None

        if enable_devices:
            self.device_coordinator = UnifiDeviceCoordinator(
                hass=hass, client=self.client, site_id=site_id
            )

        if enable_clients:
            self.client_coordinator = UnifiClientCoordinator(
                hass=hass, client=self.client, site_id=site_id
            )

    async def async_init(self) -> None:
        """Initialize data and start updates."""
        if self.device_coordinator:
            await self.device_coordinator.async_config_entry_first_refresh()
        if self.client_coordinator:
            await self.client_coordinator.async_config_entry_first_refresh()
