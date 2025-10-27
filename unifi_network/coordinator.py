from __future__ import annotations
from dataclasses import dataclass
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
from .api_client.models import DeviceOverview, LatestStatisticsForADevice

_LOGGER = logging.getLogger(__name__)


@dataclass
class UnifiDevice:
    """Represents a Unifi device with its overview and statistics."""

    overview: DeviceOverview
    latest_statistics: LatestStatisticsForADevice | None


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
    statistics for each device concurrently, storing both in UnifiDevice objects
    in a dict mapping device_id to UnifiDevice.
    """

    def __init__(self, hass: HomeAssistant, client: Client, site_id: str):
        super().__init__(
            hass=hass,
            client=client,
            site_id=site_id,
            name="devices",
            update_method=self._fetch_and_merge,
        )

    async def _fetch_and_merge(self):
        """Fetch devices and their latest statistics, merge and return dict."""
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

            # Create UnifiDevice objects combining overview and statistics
            unifi_devices = {}
            for device, res in zip(devices, results):
                device_id = getattr(device, "id", None)
                if device_id is None:
                    _LOGGER.warning("Device without id found, skipping")
                    continue
                    
                if isinstance(res, Exception):
                    _LOGGER.debug("Failed to fetch stats for device %s: %s", device_id, res)
                    stats = None
                else:
                    _LOGGER.debug("Fetched stats for device %s", device_id)
                    stats = res
                
                unifi_devices[device_id] = UnifiDevice(
                    overview=device,
                    latest_statistics=stats,
                )

            return unifi_devices

        except Exception as err:
            raise UpdateFailed(f"Error fetching devices or statistics: {err}")

