from __future__ import annotations

from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client.types import UNSET
from .const import DOMAIN
from .coordinator import UnifiClientCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Unifi device_tracker platform."""
    core = hass.data[DOMAIN][entry.entry_id]
    coordinator = core.client_coordinator

    # Keep track of client IDs that already got entities
    tracked_clients: set[str] = set()

    def _discover_new_clients() -> None:
        """Check coordinator data and add entities for new clients."""
        if not coordinator.data:
            return

        new_entities = []

        for client_id in coordinator.data:
            if client_id in tracked_clients:
                continue

            new_entities.append(UnifiClientTracker(coordinator, client_id))
            tracked_clients.add(client_id)

        if new_entities:
            async_add_entities(new_entities)

    # Add initial clients
    _discover_new_clients()

    # Add new clients whenever coordinator updates
    coordinator.async_add_listener(_discover_new_clients)


class UnifiClientTracker(CoordinatorEntity, TrackerEntity):
    """Represents a Unifi client tracker (state based on client connection status)."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_source_type = SourceType.ROUTER  # Mark this as router-based tracking

    def __init__(self, coordinator: UnifiClientCoordinator, client_id: str) -> None:
        super().__init__(coordinator)
        self.client_id = client_id
        self._attr_unique_id = f"unifi_client_{client_id}_device_tracker"

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Enable new trackers by default."""
        return True

    @property
    def state(self) -> str:
        # coordinator.data is a dict of client wrappers; presence implies connected
        client = self.coordinator.get_client(self.client_id)
        return "home" if client else "not_home"

    @property
    def device_info(self) -> DeviceInfo | None:
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None

        return DeviceInfo(
            identifiers={(DOMAIN, self.client_id)},
            name=client.name,
            model=getattr(client.overview, "type_", None),
            connections={(CONNECTION_NETWORK_MAC, client.mac)} if client.mac else set(),
            manufacturer=getattr(client, "vendor", None),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the client tracker.

        Include IP address, MAC and connected_at time.
        """
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None
        attrs = {"mac": client.mac, "ip": client.ip}

        connected_at = getattr(client.overview, "connected_at", None)
        if connected_at is not None and connected_at is not UNSET:
            attrs["connected_at"] = connected_at

        return attrs
