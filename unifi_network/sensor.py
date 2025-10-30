from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api_client.models.device_overview_interfaces_item import (
    DeviceOverviewInterfacesItem,
)
from .api_client.models.device_overview_state import DeviceOverviewState
from .api_client.types import UNSET
from .const import DOMAIN
from .coordinator import UnifiDeviceCoordinator
from .unifi_device import UnifiDevice


# Subclass SensorEntityDescription to add sensor_type
@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription):
    """Extended sensor entity description with sensor_type reference."""

    sensor_type: type[UnifiDeviceSensor]  # reference to the class to instantiate


class UnifiDeviceSensor(CoordinatorEntity, SensorEntity):
    """Represents a specific statistic for a Unifi device."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Unifi device sensor."""
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
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        value = getattr(device.latest_statistics, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value


class UnifiDeviceStateSensor(UnifiDeviceSensor):
    """Represents the state of a Unifi device."""

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device:
            return None
        state = getattr(device.overview, "state", None)
        if state is None or state is UNSET:
            return None
        if isinstance(state, DeviceOverviewState):
            return state.value.lower().replace("_", " ").title()
        return str(state)


class UnifiDeviceUplinkSensor(UnifiDeviceSensor):
    """Represents an uplink statistic for a Unifi device."""

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
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

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
        description: SensorEntityDescription,
        frequency_ghz: float,
    ) -> None:
        """Initialize the Unifi device radio sensor."""
        UnifiDeviceSensor.__init__(self, coordinator, device_id, description)
        self._frequency_ghz = frequency_ghz
        self._attr_unique_id = (
            f"unifi_device_{device_id}_{frequency_ghz}_{description.key}"
        )
        self._attr_translation_placeholders = {"frequencyGHz": str(frequency_ghz)}

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        interfaces_obj = getattr(device.latest_statistics, "interfaces", None)
        if not interfaces_obj:
            return None
        value = None
        for radio in getattr(interfaces_obj, "radios", []):
            frequency_ghz = getattr(radio, "frequency_g_hz", None)
            if frequency_ghz == self._frequency_ghz:
                # Found the matching radio
                value = getattr(radio, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value


# Define sensor descriptions after the sensor classes so referenced classes exist
DEVICE_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStateSensor,
        key="state",
        translation_key="state",
        icon="mdi:state-machine",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
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
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cpu-64-bit",
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="memory_utilization_pct",
        translation_key="memory_utilization_pct",
        native_unit_of_measurement="%",
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


def _create_base_sensors(
    device: UnifiDevice,
    device_coordinator: UnifiDeviceCoordinator,
    descriptions: tuple[UnifiSensorEntityDescription, ...],
) -> list[UnifiDeviceSensor]:
    """Create standard sensors for a device."""
    overview = device.overview

    return [
        description.sensor_type(
            device_coordinator,
            overview.id,
            description,
        )
        for description in descriptions
    ]


def _create_radio_sensors(
    device: UnifiDevice,
    device_coordinator: UnifiDeviceCoordinator,
    descriptions: tuple[UnifiSensorEntityDescription, ...],
) -> list[UnifiDeviceSensor]:
    """Create radio frequency sensors if radio interface statistics are available."""
    overview = device.overview

    interfaces = getattr(overview, "interfaces", None)
    if not interfaces or DeviceOverviewInterfacesItem.RADIOS not in interfaces:
        return []

    stats = device.latest_statistics
    if not stats:
        return []

    interfaces_obj = getattr(stats, "interfaces", None)
    if not interfaces_obj:
        return []

    radios = getattr(interfaces_obj, "radios", [])
    if not radios:
        return []

    entities: list[UnifiDeviceSensor] = []

    for radio in radios:
        frequency = getattr(radio, "frequency_g_hz", None)
        if not frequency:
            continue

        for description in descriptions:
            entities.append(
                description.sensor_type(
                    device_coordinator,
                    overview.id,
                    description,
                    frequency,
                )
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Unifi Network sensors from a config entry."""
    core = hass.data[DOMAIN][entry.entry_id]
    device_coordinator = core.device_coordinator
    devices = (
        device_coordinator.data
        if device_coordinator and device_coordinator.data
        else {}
    )

    entities: list[SensorEntity] = []
    for device in devices.values():
        entities.extend(
            _create_base_sensors(
                device,
                device_coordinator,
                DEVICE_SENSOR_DESCRIPTIONS,
            )
        )
        entities.extend(
            _create_radio_sensors(
                device,
                device_coordinator,
                DEVICE_RADIO_SENSOR_DESCRIPTIONS,
            )
        )
    async_add_entities(entities)
