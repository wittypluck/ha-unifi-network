from __future__ import annotations
from datetime import timedelta
import asyncio
import logging
from typing import Any, Callable, Coroutine

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api_client import Client
from .api_client.api.uni_fi_devices import (
    get_device_overview_page,
    get_device_latest_statistics,
)

_LOGGER = logging.getLogger(__name__)


class UnifiCoordinator(DataUpdateCoordinator):
    """Manages data updates from Unifi Network API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Client,
        site_id: str,
        name: str,
        update_method: Callable[[], Coroutine[Any, Any, Any]]
    ):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )
        self.client = client
        self.site_id = site_id
        self._update_method = update_method

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        return await self._update_method()


class UnifiDeviceCoordinator(UnifiCoordinator):
    """Coordinator specialized for devices + latest statistics.

    This class fetches the device overview page and then retrieves the latest
    statistics for each device concurrently, storing the statistics in a dict
    mapping device_id to stats.
    """

    def __init__(self, hass: HomeAssistant, client: Client, site_id: str):
        super().__init__(
            hass=hass,
            client=client,
            site_id=site_id,
            name="devices",
            update_method=self._fetch_and_merge,
        )
        self._latest_stats = {}

    @property
    def latest_stats(self):
        return self._latest_stats

    async def _fetch_and_merge(self):
        """Fetch devices and their latest statistics, merge and return list."""
        try:
            response = await get_device_overview_page.asyncio_detailed(
                client=self.client, site_id=self.site_id
            )
            if response is None or response.status_code != 200:
                raise UpdateFailed(f"Device overview API returned {getattr(response, 'status_code', None)}")

            devices = response.parsed.data or []

            # Prepare tasks to fetch statistics for each device concurrently
            tasks = [
                get_device_latest_statistics.asyncio(
                    site_id=self.site_id,
                    device_id=device.id,
                    client=self.client,
                )
                for device in devices
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Store statistics (or None) in a dict by device id
            # TODO attach stats directly to device objects
            self._latest_stats = {}
            for device, res in zip(devices, results):
                if isinstance(res, Exception):
                    _LOGGER.debug("Failed to fetch stats for device %s: %s", getattr(device, "id", None), res)
                    self._latest_stats[getattr(device, "id", None)] = None
                else:
                    _LOGGER.debug("Fetched stats for device %s: %s", getattr(device, "id", None), res)
                    self._latest_stats[getattr(device, "id", None)] = res

            return devices

        except Exception as err:
            raise UpdateFailed(f"Error fetching devices or statistics: {err}")

