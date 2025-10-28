from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Type

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .api_client.types import UNSET
from .api_client.models.device_overview_interfaces_item import DeviceOverviewInterfacesItem
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.const import UnitOfDataRate

from .coordinator import UnifiDeviceCoordinator

# Subclass SensorEntityDescription to add sensor_type
@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription):
    sensor_type: Type[Any]  # reference to the class to instantiate

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices_dict = coordinator.device_coordinator.data if coordinator.device_coordinator and coordinator.device_coordinator.data else {}

    entities: list[SensorEntity] = []
    for device_id, device in devices_dict.items():
        device_overview = device.overview
        for description in DEVICE_SENSOR_DESCRIPTIONS:
            entities.append(
                description.sensor_type(
                    coordinator.device_coordinator,
                    device_overview.id,
                    device_overview.name,
                    description,
                )
            )
        #Check if device has interfaces
        interfaces = getattr(device_overview, "interfaces", None)
        if interfaces:
            #Check if device has radio interfaces
            if DeviceOverviewInterfacesItem.RADIOS in interfaces:
                # Access statistics from UnifiDevice
                stats = device.latest_statistics
                if stats:
                    interfaces_obj = getattr(stats, "interfaces", None)
                    if interfaces_obj:
                        for radio in getattr(interfaces_obj, "radios", []):
                            #Create a set of sensors for each radio frequency
                            frequencyGHz = getattr(radio, "frequency_g_hz", None)
                            if frequencyGHz:
                                for description in DEVICE_RADIO_SENSOR_DESCRIPTIONS:
                                    entities.append(
                                        description.sensor_type(
                                            coordinator.device_coordinator,
                                            device_overview.id,
                                            device_overview.name,
                                            description,
                                            frequencyGHz,
                                        )
                                    )
    async_add_entities(entities)


class UnifiDeviceSensor(CoordinatorEntity, SensorEntity):
    """Represents a specific statistic for a Unifi device."""


    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: UnifiDeviceCoordinator, device_id: Any, device_name: str, description: SensorEntityDescription):
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = description
        self.device_id = device_id
        self._attr_unique_id = f"unifi_device_{device_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device registry information for this device (same as base sensor)."""
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

class UnifiDeviceStatisticSensor(UnifiDeviceSensor):
    """Represents a base level statistic for a Unifi device."""

    @property
    def native_value(self):
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        value = getattr(device.latest_statistics, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

class UnifiDeviceUplinkSensor(UnifiDeviceSensor):
    """Represents an uplink statistic for a Unifi device."""

    @property
    def native_value(self):
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        uplink_obj = getattr(device.latest_statistics, "uplink", None)
        if not uplink_obj:
            return None
        value = getattr(uplink_obj, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

class UnifiDeviceRadioSensor(UnifiDeviceSensor):
    """Represents a radio statistic for a Unifi device."""
    
    def __init__(self, coordinator: UnifiDeviceCoordinator, device_id: Any, device_name: str, description: SensorEntityDescription, frequencyGHz: float):
        UnifiDeviceSensor.__init__(self, coordinator, device_id, device_name, description)
        self._frequencyGHz = frequencyGHz
        self._attr_unique_id = f"unifi_device_{device_id}_{frequencyGHz}_{description.key}"
        self._attr_translation_placeholders = {"frequencyGHz": str(frequencyGHz)}

    @property
    def native_value(self):
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        interfaces_obj = getattr(device.latest_statistics, "interfaces", None)
        if not interfaces_obj:
            return None
        value = None
        for radio in getattr(interfaces_obj, "radios", []):
            frequencyGHz = getattr(radio, "frequency_g_hz", None)
            if frequencyGHz == self._frequencyGHz:
                # Found the matching radio
                value = getattr(radio, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

# Define sensor descriptions after the sensor classes so referenced classes exist
DEVICE_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="uptime_sec",
        translation_key="uptime_sec",
        native_unit_of_measurement="s",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer-outline",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_1_min",
        translation_key="load_average_1_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_5_min",
        translation_key="load_average_5_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_15_min",
        translation_key="load_average_15_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-line",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="cpu_utilization_pct",
        translation_key="cpu_utilization_pct",
        native_unit_of_measurement="%",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cpu-64-bit",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="memory_utilization_pct",
        translation_key="memory_utilization_pct",
        native_unit_of_measurement="%",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:memory",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceUplinkSensor,
        key="rx_rate_bps",
        translation_key="uplink_rx_rate_bps",
        native_unit_of_measurement=UnitOfDataRate.BITS_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:download",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceUplinkSensor,
        key="tx_rate_bps",
        translation_key="uplink_tx_rate_bps",
        native_unit_of_measurement=UnitOfDataRate.BITS_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:upload",
    ),
)
# Define sensor descriptions after the sensor classes so referenced classes exist
DEVICE_RADIO_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceRadioSensor,
        key="tx_retries_pct",
        translation_key="tx_retries_pct",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:wifi-sync",
    ),
)