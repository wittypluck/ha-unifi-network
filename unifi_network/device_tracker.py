from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up Unifi device_tracker platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = coordinator.device_coordinator.data or []

    entities: list[UnifiDeviceTracker] = []
    for device in devices:
        entities.append(UnifiDeviceTracker(coordinator.device_coordinator, device.id, device.name))

    async_add_entities(entities)


def _find_device(coordinator, device_id: Any):
    """Find the current device object by id from coordinator data."""
    devices = coordinator.data or []
    for d in devices:
        if getattr(d, "id", None) == device_id:
            return d
    return None


class UnifiDeviceTracker(CoordinatorEntity):
    """Represents a Unifi device tracker (state based on device status)."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC


    def __init__(self, coordinator, device_id: Any, device_name: str):
        super().__init__(coordinator)
        self.device_id = device_id
        self.device_name = device_name
        self._attr_unique_id = f"unifi_device_{device_id}_device_tracker"

    @property
    def state(self):
        # coordinator.data is a list of device objects; use _find_device to locate by id
        device = _find_device(self.coordinator, self.device_id)
        if not device:
            return "unknown"
        dev_state = getattr(device, "state", None)
        if dev_state is None:
            return "unknown"
        if dev_state == "ONLINE":
            return "home"
        if dev_state == "OFFLINE":
            return "not_home"
        return "unknown"

    @property
    def device_info(self):
        device = _find_device(self.coordinator, self.device_id)
        if not device:
            return None
        mac = getattr(device, "mac_address", None)
        model = getattr(device, "model", None)
        identifiers = {(DOMAIN, str(getattr(device, "id", self.device_id)))}
        connections = {(CONNECTION_NETWORK_MAC, mac)} if mac else set()
        return DeviceInfo(
            identifiers=identifiers,
            name=getattr(device, "name", None),
            model=model,
            connections=connections,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the device tracker.

        Include IP address, MAC and source_type so other integrations and
        automations can rely on them.
        """
        device = _find_device(self.coordinator, self.device_id)
        if not device:
            return None
        ip = getattr(device, "ip_address", None)
        mac = getattr(device, "mac_address", None)
        return {
            "ip": ip,
            "mac": mac,
            "source_type": "router",
        }

