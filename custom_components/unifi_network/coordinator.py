from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Coroutine
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api_client import Client
from .api_client.api.clients import get_connected_client_overview_page
from .api_client.api.uni_fi_devices import (
    get_adopted_device_details,
    get_adopted_device_latest_statistics,
    get_adopted_device_overview_page,
)
from .api_helpers import fetch_all_pages
from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN
from .unifi_client import UnifiClient
from .unifi_device import UnifiDevice

_LOGGER = logging.getLogger(__name__)


class UnifiCoordinator(DataUpdateCoordinator):
    """Manages data updates from Unifi Network API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Client,
        site_id: str,
        name: str,
        update_method: Callable[[], Coroutine[Any, Any, Any]],
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

    async def _async_update_data(self) -> dict[str, Any]:
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

    def get_device(self, device_id: str) -> UnifiDevice | None:
        """Return the cached UnifiDevice by id, if present."""
        data = self.data or {}
        return data.get(device_id)

    async def _fetch_and_merge(self) -> dict[str, UnifiDevice]:
        """Fetch devices and their latest statistics, merge and return dict."""
        try:
            # Fetch all devices using pagination helper
            device_overviews = await fetch_all_pages(
                get_adopted_device_overview_page.asyncio_detailed,
                client=self.client,
                site_id=self.site_id,
            )

            # Prepare tasks to fetch statistics and details for each device concurrently
            stats_tasks = [
                get_adopted_device_latest_statistics.asyncio(
                    site_id=self.site_id,
                    device_id=device_overview.id,
                    client=self.client,
                )
                for device_overview in device_overviews
            ]

            details_tasks = [
                get_adopted_device_details.asyncio(
                    site_id=self.site_id,
                    device_id=device_overview.id,
                    client=self.client,
                )
                for device_overview in device_overviews
            ]

            stats_results = await asyncio.gather(*stats_tasks, return_exceptions=True)
            details_results = await asyncio.gather(
                *details_tasks, return_exceptions=True
            )

            # Create UnifiDevice objects combining overview, statistics, and details
            unifi_devices = {}
            for device_overview, stats_res, details_res in zip(
                device_overviews, stats_results, details_results, strict=False
            ):
                if not hasattr(device_overview, "id") or device_overview.id is None:
                    _LOGGER.warning("Device without id found, skipping")
                    continue

                device = UnifiDevice(
                    overview=device_overview,
                    latest_statistics=None,
                    details=None,
                )
                device_id = device.id  # Always a string via the property

                if isinstance(stats_res, Exception):
                    _LOGGER.debug(
                        "Failed to fetch stats for device %s: %s", device_id, stats_res
                    )
                    device.latest_statistics = None
                else:
                    _LOGGER.debug("Fetched stats for device %s", device_id)
                    device.latest_statistics = stats_res

                if isinstance(details_res, Exception):
                    _LOGGER.debug(
                        "Failed to fetch details for device %s: %s",
                        device_id,
                        details_res,
                    )
                    device.details = None
                else:
                    _LOGGER.debug("Fetched details for device %s", device_id)
                    device.details = details_res

                unifi_devices[device_id] = device

            return unifi_devices

        except Exception as err:
            raise UpdateFailed("Error fetching devices or statistics") from err


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
        # Keep track of all clients ever seen
        self.known_clients: dict[str, UnifiClient] = {}

    def get_client(self, client_id: str) -> UnifiClient | None:
        """Return the cached UnifiClient by id, even if offline."""
        return self.known_clients.get(client_id)

    async def _fetch_and_merge(self) -> dict[str, UnifiClient]:
        """Fetch clients and their details, merge and return dict."""
        try:
            # Fetch all clients using pagination helper
            client_overviews = await fetch_all_pages(
                get_connected_client_overview_page.asyncio_detailed,
                client=self.client,
                site_id=self.site_id,
            )

            # Prepare tasks to fetch details for each client concurrently
            # tasks = [
            #    get_connected_client_details.asyncio(
            #        site_id=self.site_id,
            #        client_id=client_overview.id,
            #        client=self.client,
            #    )
            #    for client_overview in client_overviews
            # ]

            # results = await asyncio.gather(*tasks, return_exceptions=True)

            # Create UnifiClient objects combining overview and details
            unifi_clients: dict[str, UnifiClient] = {}
            now = dt_util.now()

            # for client_overview, res in zip(client_overviews, results, strict=False):
            for client_overview in client_overviews:
                if not hasattr(client_overview, "id") or client_overview.id is None:
                    _LOGGER.warning("Client without id found, skipping")
                    continue

                client = UnifiClient(overview=client_overview, details=None)
                client_id = client.id  # Always a string via the property

                # if isinstance(res, Exception):
                #    _LOGGER.debug(
                #        "Failed to fetch details for client %s: %s", client_id, res
                #    )
                #    client.details = None
                # else:
                #    _LOGGER.debug("Fetched details for client %s", client_id)
                #    client.details = res

                client.last_seen = now

                unifi_clients[client_id] = client

                # Merge into known_clients
                if client_id in self.known_clients:
                    self.known_clients[client_id].update(client)
                else:
                    self.known_clients[client_id] = client

            return unifi_clients

        except Exception as err:
            raise UpdateFailed("Error fetching clients or details") from err
