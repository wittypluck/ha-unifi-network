"""Update platform for UniFi Network devices."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UnifiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up UniFi Network update entities."""
    core = hass.data[DOMAIN][config_entry.entry_id]

    if not core.device_coordinator:
        return

    coordinator: UnifiDeviceCoordinator = core.device_coordinator

    entities: list[UnifiUpdateEntity] = []

    # Create update entity for each device
    if coordinator.data:
        for device_id, device in coordinator.data.items():
            if device.details:  # Only create update entity if we have device details
                entities.append(
                    UnifiUpdateEntity(
                        coordinator=coordinator,
                        device_id=device_id,
                    )
                )

    async_add_entities(entities)


class UnifiUpdateEntity(CoordinatorEntity, UpdateEntity):
    """Update entity for UniFi devices to show firmware information."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_supported_features = UpdateEntityFeature.INSTALL

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
    ) -> None:
        """Initialize the UniFi update entity."""
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_unique_id = f"unifi_device_{device_id}_firmware_update"
        self._attr_translation_key = "firmware_update"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device registry information for this device."""
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        return device.device_info

    @property
    def installed_version(self) -> str | None:
        """Return the currently installed version."""
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        return device.firmware_version

    @property
    def latest_version(self) -> str | None:
        """Return the latest available version.

        Note: UniFi API doesn't provide specific version information for available
        updates. We return the current version if no update is available, or
        "Unknown" if an update is available but we don't know the version.
        """
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None

        # If firmware is updatable, we know there's a newer version but don't know which
        if device.firmware_updatable:
            return "Unknown"

        # If not updatable, current version is the latest
        return device.firmware_version

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        device = self.coordinator.get_device(self.device_id)
        return device is not None and device.firmware_version is not None

    @property
    def title(self) -> str | None:
        """Return the title of the software/firmware."""
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        return f"{device.name or 'UniFi Device'} Firmware"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return {}

        attributes = {}

        # Add device model for context
        if device.overview and hasattr(device.overview, "model"):
            attributes["device_model"] = device.overview.model

        return attributes

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Install firmware update.

        Note: This integration currently doesn't support triggering firmware updates
        through the API. Users should update firmware through the UniFi Network
        Application interface.
        """
        _LOGGER.warning(
            "Firmware update installation not supported. "
            "Please use the UniFi Network Application to update device firmware."
        )
        raise NotImplementedError(
            "Firmware update installation is not supported by this integration. "
            "Please use the UniFi Network Application to update device firmware."
        )
