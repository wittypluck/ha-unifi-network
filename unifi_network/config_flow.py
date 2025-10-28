from __future__ import annotations
import logging
from homeassistant import config_entries
from homeassistant.helpers import selector
import voluptuous as vol
from aiohttp import ClientError

from .const import DOMAIN
from .api_client import Client
from .api_client.api.sites import get_site_overview_page
from .api_helpers import fetch_all_pages

_LOGGER = logging.getLogger(__name__)

class UnifiNetworkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Unifi Network integration."""
    VERSION = 1

    def __init__(self):
        self._base_url = None
        self._api_key = None
        self._sites = None
        self._selected_site_id = None
        self._selected_site_name = None

    async def async_step_user(self, user_input=None):
        """First step: ask for base URL and API key."""
        errors = {}

        if user_input is not None:
            base_url = user_input["base_url"]
            api_key = user_input["api_key"]
            self._base_url = base_url
            self._api_key = api_key

            # Try to fetch sites using pagination helper
            try:
                headers = {"X-API-Key": api_key} if api_key else None
                client = Client(base_url=base_url, headers=headers)
                
                # Fetch all sites
                all_sites = await fetch_all_pages(
                    get_site_overview_page.asyncio_detailed,
                    client=client
                )

                if not all_sites:
                    raise ClientError("No sites returned by API")

                self._sites = {site.name: site.id for site in all_sites}

                return await self.async_step_select_site()

            except Exception as err:
                _LOGGER.exception("Error connecting to Unifi API: %s", err)
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required("base_url"): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.URL)
            ),
            vol.Required("api_key"): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
            ),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_select_site(self, user_input=None):
        """Second step: user chooses one site by name."""
        errors = {}

        if user_input is not None:
            site_name = user_input["site_name"]
            site_id = self._sites.get(site_name)
            if site_id:
                self._selected_site_id = site_id
                self._selected_site_name = site_name
                return await self.async_step_select_features()
            else:
                errors["base"] = "invalid_site"

        schema = vol.Schema({
            vol.Required("site_name"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=list(self._sites.keys()))
            ),
        })

        return self.async_show_form(step_id="select_site", data_schema=schema, errors=errors)

    async def async_step_select_features(self, user_input=None):
        """Third step: user selects which features to enable."""
        errors = {}

        if user_input is not None:
            enable_devices = user_input.get("enable_devices", False)
            enable_clients = user_input.get("enable_clients", False)

            if not enable_devices and not enable_clients:
                errors["base"] = "no_features_selected"
            else:
                return self.async_create_entry(
                    title=f"Unifi: {self._selected_site_name}",
                    data={
                        "base_url": self._base_url,
                        "api_key": self._api_key,
                        "site_id": self._selected_site_id,
                        "site_name": self._selected_site_name,
                        "enable_devices": enable_devices,
                        "enable_clients": enable_clients,
                    },
                )

        schema = vol.Schema({
            vol.Optional("enable_devices", default=True): selector.BooleanSelector(),
            vol.Optional("enable_clients", default=True): selector.BooleanSelector(),
        })

        return self.async_show_form(step_id="select_features", data_schema=schema, errors=errors)
