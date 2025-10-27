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
from .api_client.api.clients import (
    get_connected_client_overview_page,
    get_connected_client_details,
)
from .api_client.models import (
    DeviceOverview,
    LatestStatisticsForADevice,
    ClientOverview,
    ClientDetails,
)

_LOGGER = logging.getLogger(__name__)


@dataclass
class UnifiDevice:
    """Represents a Unifi device with its overview and statistics."""

    overview: DeviceOverview
    latest_statistics: LatestStatisticsForADevice | None

    @property
    def name(self) -> str | None:
        """Return the device name."""
        return getattr(self.overview, "name", None)

    @property
    def ip(self) -> str | None:
        """Return the device IP address."""
        return getattr(self.overview, "ip_address", None)

    @property
    def mac(self) -> str | None:
        """Return the device MAC address."""
        return getattr(self.overview, "mac_address", None)


@dataclass
class UnifiClient:
    """Represents a Unifi client with its overview and details."""

    overview: ClientOverview
    details: ClientDetails | None

    @property
    def name(self) -> str | None:
        """Return the client name."""
        return getattr(self.overview, "name", None)

    @property
    def ip(self) -> str | None:
        """Return the client IP address."""
        return getattr(self.overview, "ip_address", None)

    @property
    def mac(self) -> str | None:
        """Return the MAC address for this client.

        The OpenAPI models keep unrecognized fields in `additional_properties`.
        UniFi currently exposes the MAC under the key "macAddress".
        """
        # Prefer value from overview, then fall back to details if present
        for src in (self.overview, self.details):
            if not src:
                continue
            additional = getattr(src, "additional_properties", None)
            if isinstance(additional, dict):
                mac = additional.get("macAddress")
                if mac:
                    return mac
        return None


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

    def get_device(self, device_id: Any) -> UnifiDevice | None:
        """Return the cached UnifiDevice by id, if present."""
        data = self.data or {}
        return data.get(device_id)

    async def _fetch_and_merge(self):
        """Fetch devices and their latest statistics, merge and return dict."""
        try:
            response = await get_device_overview_page.asyncio_detailed(
                client=self.client, site_id=self.site_id
            )
            if response is None or response.status_code != 200:
                raise UpdateFailed(f"Device overview API returned {getattr(response, 'status_code', None)}")

            device_overviews = response.parsed.data or []

            # Prepare tasks to fetch statistics for each device concurrently
            tasks = [
                get_device_latest_statistics.asyncio(
                    site_id=self.site_id,
                    device_id=device_overview.id,
                    client=self.client,
                )
                for device_overview in device_overviews
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Create UnifiDevice objects combining overview and statistics
            unifi_devices = {}
            for device_overview, res in zip(device_overviews, results):
                device_id = getattr(device_overview, "id", None)
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
                    overview=device_overview,
                    latest_statistics=stats,
                )

            return unifi_devices

        except Exception as err:
            raise UpdateFailed(f"Error fetching devices or statistics: {err}")


class UnifiClientCoordinator(UnifiCoordinator):
    """Coordinator specialized for clients + details.

    This class fetches the client overview page and then retrieves the details
    for each client concurrently, storing both in UnifiClient objects
    in a dict mapping client_id to UnifiClient.
    """

    def __init__(self, hass: HomeAssistant, client: Client, site_id: str):
        super().__init__(
            hass=hass,
            client=client,
            site_id=site_id,
            name="clients",
            update_method=self._fetch_and_merge,
        )

    def get_client(self, client_id: Any) -> UnifiClient | None:
        """Return the cached UnifiClient by id, if present."""
        data = self.data or {}
        return data.get(client_id)

    async def _fetch_and_merge(self):
        """Fetch clients and their details, merge and return dict."""
        try:
            response = await get_connected_client_overview_page.asyncio_detailed(
                client=self.client, site_id=self.site_id
            )
            if response is None or response.status_code != 200:
                raise UpdateFailed(f"Client overview API returned {getattr(response, 'status_code', None)}")

            client_overviews = response.parsed.data or []

            # Prepare tasks to fetch details for each client concurrently
            tasks = [
                get_connected_client_details.asyncio(
                    site_id=self.site_id,
                    client_id=client_overview.id,
                    client=self.client,
                )
                for client_overview in client_overviews
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Create UnifiClient objects combining overview and details
            unifi_clients = {}
            for client_overview, res in zip(client_overviews, results):
                client_id = getattr(client_overview, "id", None)
                if client_id is None:
                    _LOGGER.warning("Client without id found, skipping")
                    continue
                    
                if isinstance(res, Exception):
                    _LOGGER.debug("Failed to fetch details for client %s: %s", client_id, res)
                    details = None
                else:
                    _LOGGER.debug("Fetched details for client %s", client_id)
                    details = res
                
                unifi_clients[client_id] = UnifiClient(
                    overview=client_overview,
                    details=details,
                )

            return unifi_clients

        except Exception as err:
            raise UpdateFailed(f"Error fetching clients or details: {err}")

