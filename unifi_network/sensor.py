from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfDataRate, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .api_client.models.device_overview_interfaces_item import (
    DeviceOverviewInterfacesItem,
)
from .api_client.models.device_overview_state import DeviceOverviewState
from .api_client.models.port_overview import PortOverview
from .api_client.models.port_po_e_overview import PortPoEOverview
from .api_client.types import UNSET
from .const import DOMAIN
from .coordinator import UnifiClientCoordinator, UnifiDeviceCoordinator
from .unifi_client import UnifiClient
from .unifi_device import UnifiDevice


# --- Base classes ---
@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription):
    """Extended sensor entity description with sensor_type reference."""

    sensor_type: type[
        UnifiDeviceSensor | UnifiClientSensor
    ]  # reference to the class to instantiate


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


class UnifiDeviceUptimeSensor(UnifiDeviceSensor):
    """Represents an uptime sensor for a Unifi device."""

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        # Access UnifiDevice from coordinator accessor
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.latest_statistics:
            return None
        uptime_sec = device.latest_statistics.uptime_sec
        if uptime_sec is None or uptime_sec is UNSET:
            return None
        boot_time = dt_util.now() - timedelta(seconds=uptime_sec)
        # Return boot time rounded to the nearest minute
        return boot_time.replace(second=0, microsecond=0)


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
            f"unifi_device_{device_id}_radio_{frequency_ghz}_{description.key}"
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


class UnifiDevicePortSensor(UnifiDeviceSensor):
    """Represents a port sensor for a Unifi device."""

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
        description: SensorEntityDescription,
        port_idx: int,
    ) -> None:
        """Initialize the Unifi device port sensor."""
        UnifiDeviceSensor.__init__(self, coordinator, device_id, description)
        self._port_idx = port_idx
        self._attr_unique_id = (
            f"unifi_device_{device_id}_port_{port_idx}_{description.key}"
        )
        self._attr_translation_placeholders = {"portIdx": str(port_idx)}

    @property
    def native_value(self) -> float | int | str | bool | None:
        """Return the state of the sensor (non-POE keys only)."""
        port = self._get_port()
        if port is None:
            return None
        value = getattr(port, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

    def _get_port(self) -> PortOverview | None:
        device = self.coordinator.get_device(self.device_id)
        if not device or not device.details:
            return None
        interfaces_obj = getattr(device.details, "interfaces", None)
        if not interfaces_obj:
            return None
        ports = getattr(interfaces_obj, "ports", [])
        if not ports or ports is UNSET:
            return None
        for port in ports:
            port_idx = getattr(port, "idx", None)
            if port_idx == self._port_idx:
                return port
        return None


class UnifiDevicePortStateSensor(UnifiDevicePortSensor):
    """Represents the state of a Unifi device port."""

    @property
    def native_value(self) -> str | None:
        """Return the state of the port sensor with enum value conversion."""
        port = self._get_port()
        if port is None:
            return None
        value = getattr(port, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        # Convert enum values to readable strings
        return str(value).lower().replace("_", " ").title()

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the state sensor:
        Port speed, port max speed.
        """
        port = self._get_port()
        if port is None:
            return None
        return {
            "port_number": port.idx,
            "port_connector": str(port.connector)
            if port.connector and port.connector is not UNSET
            else None,
            "speed_mbps": None if port.speed_mbps is UNSET else port.speed_mbps,
            "max_speed_mbps": None
            if port.max_speed_mbps is UNSET
            else port.max_speed_mbps,
        }


# POE port sensor descriptions


class UnifiDevicePortPoeSensor(UnifiDevicePortSensor):
    """Represents a POE port sensor for a Unifi device."""

    def __init__(
        self,
        coordinator: UnifiDeviceCoordinator,
        device_id: str,
        description: SensorEntityDescription,
        port_idx: int,
    ) -> None:
        """Initialize the Unifi device port sensor."""
        UnifiDevicePortSensor.__init__(
            self, coordinator, device_id, description, port_idx
        )
        self._attr_unique_id = (
            f"unifi_device_{device_id}_port_{port_idx}_poe_{description.key}"
        )

    @property
    def native_value(self) -> float | int | str | bool | None:
        """Return the state of the POE sensor."""
        poe = self._get_poe()
        if poe is None:
            return None
        value = getattr(poe, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value

    def _get_poe(self) -> PortPoEOverview | None:
        port = self._get_port()
        if port is None:
            return None
        poe = getattr(port, "poe", None)
        if not poe or poe is UNSET:
            return None
        return poe


class UnifiDevicePortPoeStateSensor(UnifiDevicePortPoeSensor):
    """Represents the state of a Unifi device port Poe."""

    @property
    def native_value(self) -> str | None:
        """Return the state of the port poe with enum value conversion."""
        poe = self._get_poe()
        if poe is None:
            return None
        value = getattr(poe, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        # Convert enum values to readable strings
        return str(value).lower().replace("_", " ").title()

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes for the state sensor:
        Port POE standard, type, and enabled status.
        """
        poe = self._get_poe()
        if poe is None:
            return None
        return {
            "poe_standard": poe.standard,
            "poe_type": str(poe.type_),
            "poe_enabled": str(poe.enabled),
        }


class UnifiClientSensor(CoordinatorEntity, SensorEntity):
    """Represents a specific sensor for a Unifi client."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: UnifiClientCoordinator,
        client_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Unifi client sensor."""
        CoordinatorEntity.__init__(self, coordinator)
        self.entity_description = description
        self.client_id = client_id
        self._attr_unique_id = f"unifi_client_{client_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device registry information for this client."""
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None
        client_overview = client.overview

        client_type = getattr(client_overview, "type_", None)
        identifiers = {(DOMAIN, self.client_id)}
        connections = {(CONNECTION_NETWORK_MAC, client.mac)} if client.mac else set()

        return DeviceInfo(
            identifiers=identifiers,
            name=client.name,
            model=client_type,
            connections=connections,
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        # Access UnifiClient from coordinator accessor
        client = self.coordinator.get_client(self.client_id)
        if not client:
            return None
        value = getattr(client.overview, self.entity_description.key, None)
        if value is None or value is UNSET:
            return None
        return value


class UnifiClientStateSensor(UnifiClientSensor):
    """Represents the connection state of a Unifi client.

    This sensor requires custom logic because clients don't have a 'state' field
    in their overview. Instead, we determine state based on presence in coordinator data.
    """

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        # Access UnifiClient from coordinator accessor
        client = self.coordinator.data.get(self.client_id)
        # If client exists in coordinator data, it's connected
        return "Connected" if client else "Disconnected"


# Define sensor descriptions after the sensor classes so referenced classes exist
DEVICE_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStateSensor,
        key="state",
        translation_key="device_state",
        device_class=SensorDeviceClass.ENUM,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceUptimeSensor,
        key="uptime_sec",
        translation_key="uptime_sec",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_1_min",
        translation_key="load_average_1_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_5_min",
        translation_key="load_average_5_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="load_average_15_min",
        translation_key="load_average_15_min",
        native_unit_of_measurement=None,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="cpu_utilization_pct",
        translation_key="cpu_utilization_pct",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceStatisticSensor,
        key="memory_utilization_pct",
        translation_key="memory_utilization_pct",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceUplinkSensor,
        key="rx_rate_bps",
        translation_key="uplink_rx_rate_bps",
        native_unit_of_measurement=UnitOfDataRate.BITS_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceUplinkSensor,
        key="tx_rate_bps",
        translation_key="uplink_tx_rate_bps",
        native_unit_of_measurement=UnitOfDataRate.BITS_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
# Define sensor descriptions after the sensor classes so referenced classes exist
DEVICE_RADIO_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDeviceRadioSensor,
        key="tx_retries_pct",
        translation_key="tx_retries_pct",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

# Port sensor descriptions
DEVICE_PORT_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDevicePortStateSensor,
        key="state",
        translation_key="port_state",
        device_class=SensorDeviceClass.ENUM,
    ),
)

# Port Poe sensor descriptions
DEVICE_PORT_POE_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiDevicePortPoeStateSensor,
        key="state",
        translation_key="port_poe_state",
        device_class=SensorDeviceClass.ENUM,
    ),
)

# Client sensor descriptions
CLIENT_SENSOR_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...] = (
    UnifiSensorEntityDescription(
        sensor_type=UnifiClientStateSensor,
        key="state",
        translation_key="client_state",
        device_class=SensorDeviceClass.ENUM,
    ),
    UnifiSensorEntityDescription(
        sensor_type=UnifiClientSensor,
        key="connected_at",
        translation_key="client_connected_at",
        device_class=SensorDeviceClass.TIMESTAMP,
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


def _create_port_sensors(
    device: UnifiDevice,
    device_coordinator: UnifiDeviceCoordinator,
    descriptions: tuple[UnifiSensorEntityDescription, ...],
    poe_descriptions: tuple[
        UnifiSensorEntityDescription, ...
    ] = DEVICE_PORT_POE_SENSOR_DESCRIPTIONS,
) -> list[UnifiDeviceSensor]:
    """Create port sensors if device has port interfaces in details. POE sensors only if port has POE attribute."""
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

    entities: list[UnifiDeviceSensor] = []

    for port in ports:
        port_idx = getattr(port, "idx", None)
        if port_idx is None:
            continue

        # Standard port sensors
        for description in descriptions:
            entities.append(
                description.sensor_type(
                    device_coordinator,
                    overview.id,
                    description,
                    port_idx,
                )
            )

        # POE sensors only if port has poe attribute
        poe_obj = getattr(port, "poe", None)
        if poe_obj is not None and poe_obj is not UNSET:
            for poe_description in poe_descriptions:
                entities.append(
                    poe_description.sensor_type(
                        device_coordinator,
                        overview.id,
                        poe_description,
                        port_idx,
                    )
                )

    return entities


def _create_client_sensors(
    client: UnifiClient,
    client_coordinator: UnifiClientCoordinator,
    descriptions: tuple[UnifiSensorEntityDescription, ...],
) -> list[UnifiClientSensor]:
    """Create sensors for a client."""
    overview = client.overview

    return [
        description.sensor_type(
            client_coordinator,
            overview.id,
            description,
        )
        for description in descriptions
    ]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Unifi Network sensors from a config entry."""
    core = hass.data[DOMAIN][entry.entry_id]
    device_coordinator = core.device_coordinator
    client_coordinator = core.client_coordinator

    devices = (
        device_coordinator.data
        if device_coordinator and device_coordinator.data
        else {}
    )
    clients = (
        client_coordinator.data
        if client_coordinator and client_coordinator.data
        else {}
    )

    entities: list[SensorEntity] = []

    # Add device sensors
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
        entities.extend(
            _create_port_sensors(
                device,
                device_coordinator,
                DEVICE_PORT_SENSOR_DESCRIPTIONS,
                DEVICE_PORT_POE_SENSOR_DESCRIPTIONS,
            )
        )

    # Add client sensors
    for client in clients.values():
        entities.extend(
            _create_client_sensors(
                client,
                client_coordinator,
                CLIENT_SENSOR_DESCRIPTIONS,
            )
        )

    async_add_entities(entities)
