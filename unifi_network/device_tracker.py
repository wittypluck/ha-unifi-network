from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UnifiClientCoordinator, UnifiDeviceCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Unifi device_tracker platform."""
    core = hass.data[DOMAIN][entry.entry_id]
    devices_dict = (
        core.device_coordinator.data
        if core.device_coordinator and core.device_coordinator.data
        else {}
    )
    clients_dict = (
        core.client_coordinator.data
        if core.client_coordinator and core.client_coordinator.data
        else {}
    )

    entities: list[UnifiDeviceTracker | UnifiClientTracker] = []

    # Add device trackers
    for device_id, unifi_device in devices_dict.items():
        entities.append(
            UnifiDeviceTracker(
                core.device_coordinator, device_id, unifi_device.overview.name
            )
        )

    # Add client trackers
    for client_id, unifi_client in clients_dict.items():
        entities.append(
            UnifiClientTracker(
                core.client_coordinator, client_id, unifi_client.overview.name
            )
        )

    async_add_entities(entities)


class UnifiDeviceTracker(CoordinatorEntity):
    """Represents a Unifi device tracker (state based on device status)."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self, coordinator: UnifiDeviceCoordinator, device_id: Any, device_name: str
    ):
        super().__init__(coordinator)
        self.device_id = device_id
        self.device_name = device_name
        self._attr_unique_id = f"unifi_device_{device_id}_device_tracker"

    @property
    def state(self):
        # Use coordinator accessor to get current device overview
        device = self.coordinator.get_device(self.device_id)
        device_overview = device.overview if device else None
        if not device_overview:
            return "unknown"
        device_state = getattr(device_overview, "state", None)
        if device_state is None:
            return "unknown"
        if device_state == "ONLINE":
            return "home"
        if device_state == "OFFLINE":
            return "not_home"
        return "unknown"

    @property
    def device_info(self):
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        device_overview = device.overview
        identifiers = {(DOMAIN, self.device_id)}
        connections = {(CONNECTION_NETWORK_MAC, device.mac)} if device.mac else set()
        return DeviceInfo(
            identifiers=identifiers,
            name=device.name,
            model=getattr(device_overview, "model", None),
            connections=connections,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the device tracker.

        Include IP address, MAC and source_type so other integrations and
        automations can rely on them.
        """
        device_wrapper = self.coordinator.get_device(self.device_id)
        if not device_wrapper:
            return None
        return {
            "ip": device_wrapper.ip,
            "mac": device_wrapper.mac,
            "source_type": "router",
        }


class UnifiClientTracker(CoordinatorEntity):
    """Represents a Unifi client tracker (state based on client connection status)."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self, coordinator: UnifiClientCoordinator, client_id: Any, client_name: str
    ):
        super().__init__(coordinator)
        self.client_id = client_id
        self.client_name = client_name
        self._attr_unique_id = f"unifi_client_{client_id}_device_tracker"

    @property
    def state(self):
        # coordinator.data is a dict of client wrappers; presence implies connected
        client = self.coordinator.get_client(self.client_id)
        return "home" if client else "not_home"

    @property
    def device_info(self):
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None
        client_type = getattr(client.overview, "type_", None)
        identifiers = {(DOMAIN, self.client_id)}
        connections = {(CONNECTION_NETWORK_MAC, client.mac)} if client.mac else set()
        return DeviceInfo(
            identifiers=identifiers,
            name=client.name,
            model=client_type,
            connections=connections,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the client tracker.

        Include IP address, MAC and source_type so other integrations and
        automations can rely on them.
        """
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None
        return {"ip": client.ip, "mac": client.mac, "source_type": "router"}
