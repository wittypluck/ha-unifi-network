from __future__ import annotations
import logging
from homeassistant import config_entries
import voluptuous as vol
from aiohttp import ClientError

from .const import DOMAIN
from .api_client import Client
from .api_client.api.sites import get_site_overview_page

_LOGGER = logging.getLogger(__name__)

class UnifiNetworkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Unifi Network integration."""
    VERSION = 1

    def __init__(self):
        self._base_url = None
        self._api_key = None
        self._sites = None

    async def async_step_user(self, user_input=None):
        """First step: ask for base URL and API key."""
        errors = {}

        if user_input is not None:
            base_url = user_input["base_url"]
            api_key = user_input["api_key"]
            self._base_url = base_url
            self._api_key = api_key

            # Try to fetch sites
            try:
                headers = {"X-API-Key": api_key} if api_key else None
                client = Client(base_url=base_url, headers=headers)
                response = await get_site_overview_page.asyncio_detailed(client=client)

                if response is None:
                    raise ClientError("No response from API")

                if response.status_code != 200:
                    raise ClientError(f"Unexpected status code {response.status_code}")

                if not response.parsed or not getattr(response.parsed, "data", None):
                    raise ClientError("No sites returned by API")

                sites = response.parsed.data
                self._sites = {site.name: site.id for site in sites}

                return await self.async_step_select_site()

            except Exception as err:
                _LOGGER.exception("Error connecting to Unifi API: %s", err)
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required("base_url", description="Base Network API URL (e.g. https://192.168.1.1/proxy/network/integration)"): str,
            vol.Required("api_key", description="API Key"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_select_site(self, user_input=None):
        """Second step: user chooses one site by name."""
        errors = {}

        if user_input is not None:
            site_name = user_input["site_name"]
            site_id = self._sites.get(site_name)
            if site_id:
                return self.async_create_entry(
                    title=f"Unifi: {site_name}",
                    data={
                        "base_url": self._base_url,
                        "api_key": self._api_key,
                        "site_id": site_id,
                        "site_name": site_name,
                    },
                )
            else:
                errors["base"] = "invalid_site"

        schema = vol.Schema({
            vol.Required("site_name"): vol.In(list(self._sites.keys()))
        })

        return self.async_show_form(step_id="select_site", data_schema=schema, errors=errors)
