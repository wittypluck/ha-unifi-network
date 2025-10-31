from __future__ import annotations

import logging
from dataclasses import dataclass
from http import HTTPStatus

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client.api.uni_fi_devices.execute_port_action import asyncio_detailed
from .api_client.models.port_action_request import PortActionRequest
from .api_client.types import UNSET
from .const import DOMAIN
from .coordinator import UnifiDeviceCoordinator
from .unifi_device import UnifiDevice

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class UnifiButtonEntityDescription(ButtonEntityDescription):
    """Extended button entity description with button_type reference."""

    button_type: type[UnifiDevicePortPoeButton]


class UnifiDevicePortPoeButton(CoordinatorEntity, ButtonEntity):
    """Represents a power cycle button for a POE port on a Unifi device."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
        description: ButtonEntityDescription,
        port_idx: int,
    ) -> None:
        """Initialize the Unifi device port POE button."""
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = description
        self.device_id = device_id
        self.port_idx = port_idx
        self._attr_unique_id = (
            f"unifi_device_{device_id}_port_{port_idx}_poe_{description.key}"
        )
        self._attr_translation_placeholders = {"portIdx": str(port_idx)}

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device registry information for this device."""
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        device_overview = device.overview

        model = getattr(device_overview, "model", None)
        identifiers = {(DOMAIN, self.device_id)}
        connections = {(CONNECTION_NETWORK_MAC, device.mac)} if device.mac else set()

        return DeviceInfo(
            identifiers=identifiers,
            name=device.name,
            model=model,
            connections=connections,
        )

    @property
    def available(self) -> bool:
        """Return if button is available."""
        if not super().available:
            return False

        # Check if port exists and has POE capability
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.details:
            return False

        interfaces_obj = getattr(device.details, "interfaces", None)
        if not interfaces_obj:
            return False

        ports = getattr(interfaces_obj, "ports", [])
        if not ports or ports is UNSET:
            return False

        for port in ports:
            port_idx = getattr(port, "idx", None)
            if port_idx == self.port_idx:
                # Check if port has POE capability
                poe_obj = getattr(port, "poe", None)
                return poe_obj is not None and poe_obj is not UNSET

        return False

    async def async_press(self) -> None:
        """Handle the button press to trigger power cycle."""
        try:
            device = self.coordinator.get_device(self.device_id)
            if not device:
                _LOGGER.error("Device %s not found", self.device_id)
                return

            # Get the API client from coordinator
            api_client = self.coordinator.client
            if not api_client:
                _LOGGER.error("API client not available")
                return

            # Create the port action request for power cycle
            action_request = PortActionRequest(action="POWER_CYCLE")

            # Execute the port action using the API client
            response = await asyncio_detailed(
                site_id=self.coordinator.site_id,
                device_id=device.overview.id,
                port_idx=self.port_idx,
                client=api_client,
                body=action_request,
            )

            if response.status_code == HTTPStatus.OK:
                _LOGGER.info(
                    "Successfully triggered power cycle for device %s port %s",
                    self.device_id,
                    self.port_idx,
                )
                # Refresh device data after action
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error(
                    "Failed to trigger power cycle for device %s port %s: HTTP %s",
                    self.device_id,
                    self.port_idx,
                    response.status_code,
                )

        except Exception:
            _LOGGER.exception(
                "Error triggering power cycle for device %s port %s",
                self.device_id,
                self.port_idx,
            )


# Define button descriptions
DEVICE_PORT_POE_BUTTON_DESCRIPTIONS: tuple[UnifiButtonEntityDescription, ...] = (
    UnifiButtonEntityDescription(
        button_type=UnifiDevicePortPoeButton,
        key="power_cycle",
        translation_key="port_poe_power_cycle",
        icon="mdi:power-cycle",
    ),
)


def _create_port_poe_buttons(
    device: UnifiDevice,
    device_coordinator: UnifiDeviceCoordinator,
    descriptions: tuple[UnifiButtonEntityDescription, ...],
) -> list[UnifiDevicePortPoeButton]:
    """Create POE port buttons for device ports that have POE capability."""
    overview = device.overview

    # Check if device has details with ports
    if not device.details:
        return []

    interfaces_obj = getattr(device.details, "interfaces", None)
    if not interfaces_obj:
        return []

    ports = getattr(interfaces_obj, "ports", [])
    if not ports or ports is UNSET:
        return []

    entities: list[UnifiDevicePortPoeButton] = []

    for port in ports:
        port_idx = getattr(port, "idx", None)
        if port_idx is None:
            continue

        # POE buttons only if port has poe attribute
        poe_obj = getattr(port, "poe", None)
        if poe_obj is not None and poe_obj is not UNSET:
            for description in descriptions:
                entities.append(
                    description.button_type(
                        device_coordinator,
                        overview.id,
                        description,
                        port_idx,
                    )
                )

    return entities


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Unifi Network buttons from a config entry."""
    core = hass.data[DOMAIN][entry.entry_id]
    device_coordinator = core.device_coordinator

    devices = (
        device_coordinator.data
        if device_coordinator and device_coordinator.data
        else {}
    )

    entities: list[ButtonEntity] = []

    # Add device port POE buttons
    for device in devices.values():
        entities.extend(
            _create_port_poe_buttons(
                device,
                device_coordinator,
                DEVICE_PORT_POE_BUTTON_DESCRIPTIONS,
            )
        )

    async_add_entities(entities)
