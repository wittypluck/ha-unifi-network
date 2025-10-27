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
from .api.types import UNSET
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.const import UnitOfDataRate

# Subclass SensorEntityDescription to add sensor_type
@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription):
    sensor_type: Type[Any]  # reference to the class to instantiate

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = coordinator.device_coordinator.data or []

    entities: list[SensorEntity] = []
    for device in devices:
        for description in SENSOR_DESCRIPTIONS:
            entities.append(
                description.sensor_type(
                    coordinator.device_coordinator,
                    device.id,
                    device.name,
                    description,
                )
            )
    async_add_entities(entities)


def _find_device(coordinator, device_id: Any):
    """Find the current device object by id from coordinator data."""
    devices = coordinator.data or []
    for d in devices:
        if getattr(d, "id", None) == device_id:
            return d
    return None


class UnifiDeviceSensor(CoordinatorEntity, SensorEntity):
    """Represents a specific statistic for a Unifi device."""


    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, device_id: Any, device_name: str, description: SensorEntityDescription):
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = description
        self.device_id = device_id
        self._attr_unique_id = f"unifi_device_{device_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device registry information for this device (same as base sensor)."""
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

class UnifiDeviceStatisticSensor(UnifiDeviceSensor):
    """Represents a base level statistic for a Unifi device."""

    @property
    def native_value(self):
        # Look up statistics from the coordinator's latest_stats dict
        stats = getattr(self.coordinator, "latest_stats", None)
        if not stats:
            return None
        stat_obj = stats.get(self.device_id)
        if not stat_obj:
            return None
        value = getattr(stat_obj, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

class UnifiDeviceUplinkSensor(UnifiDeviceSensor):
    """Represents an uplink statistic for a Unifi device."""

    @property
    def native_value(self):
        # Look up statistics from the coordinator's latest_stats dict
        stats = getattr(self.coordinator, "latest_stats", None)
        if not stats:
            return None
        stat_obj = stats.get(self.device_id)
        if not stat_obj:
            return None
        uplink_obj = getattr(stat_obj, "uplink", None)
        if not uplink_obj:
            return None
        value = getattr(uplink_obj, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value


# Define sensor descriptions after the sensor classes so referenced classes exist
SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
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
        icon="mdi:memory",
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
        icon="mdi:memory",
    ),
)