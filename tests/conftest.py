"""Test configuration to mock Home Assistant dependencies."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from unittest.mock import Mock

# Mock datetime utilities
dt_util = Mock()
dt_util.now = lambda: datetime(2023, 1, 1, tzinfo=datetime.UTC)


# Mock Home Assistant core classes
class MockHomeAssistant:
    """Mock Home Assistant instance."""

    def __init__(self):
        self.data = {}


@dataclass
class MockFlowResult:
    """Mock config flow result."""

    type: str
    step_id: str | None = None
    data_schema: Any | None = None
    errors: dict[str, str] | None = None
    title: str | None = None
    data: dict[str, Any] | None = None


class MockConfigFlow:
    """Mock base config flow."""

    VERSION = 1

    def __init__(self):
        self.context = {}

    def __init_subclass__(cls, domain=None, **kwargs):
        """Handle domain parameter in subclass definition."""
        super().__init_subclass__(**kwargs)
        cls.domain = domain

    async def async_show_form(
        self,
        step_id: str,
        data_schema: Any = None,
        errors: dict[str, str] | None = None,
    ) -> MockFlowResult:
        """Mock show form."""
        return MockFlowResult(
            type="form",
            step_id=step_id,
            data_schema=data_schema,
            errors=errors or {},
        )

    async def async_create_entry(
        self, title: str, data: dict[str, Any]
    ) -> MockFlowResult:
        """Mock create entry."""
        return MockFlowResult(
            type="create_entry",
            title=title,
            data=data,
        )


class MockUpdateCoordinator:
    """Mock data update coordinator."""

    def __init__(self, hass, logger, name, update_interval):
        self.hass = hass
        self.logger = logger
        self.name = name
        self.update_interval = update_interval
        self.data = None

    async def _async_update_data(self):
        """Update data."""
        return {}


class UpdateFailed(Exception):
    """Mock UpdateFailed exception."""


# Mock config_entries module
config_entries = Mock()
config_entries.ConfigFlow = MockConfigFlow

# Mock data_entry_flow
data_entry_flow = Mock()
data_entry_flow.FlowResult = MockFlowResult

# Mock sensor components
sensor = Mock()
sensor.SensorEntity = Mock()
sensor.SensorDeviceClass = Mock()
sensor.SensorEntityDescription = Mock()
sensor.SensorStateClass = Mock()

# Mock constants
const = Mock()
const.PERCENTAGE = "%"
const.UnitOfDataRate = Mock()

# Mock entity components
entity = Mock()
entity.DeviceInfo = Mock()
entity.EntityCategory = Mock()

# Mock entity platform
entity_platform = Mock()
entity_platform.AddEntitiesCallback = Mock()

# Mock update coordinator
update_coordinator = Mock()
update_coordinator.CoordinatorEntity = Mock()
update_coordinator.DataUpdateCoordinator = MockUpdateCoordinator
update_coordinator.UpdateFailed = UpdateFailed

# Mock homeassistant modules
homeassistant = Mock()
homeassistant.config_entries = config_entries
homeassistant.core.HomeAssistant = MockHomeAssistant
homeassistant.components.sensor = sensor
homeassistant.const = const
homeassistant.helpers.entity = entity
homeassistant.helpers.entity_platform = entity_platform
homeassistant.helpers.update_coordinator = update_coordinator
homeassistant.util.dt = dt_util

# Mock homeassistant modules for import patching
sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.config_entries"] = config_entries
sys.modules["homeassistant.core"] = Mock()
sys.modules["homeassistant.const"] = const
sys.modules["homeassistant.data_entry_flow"] = data_entry_flow
sys.modules["homeassistant.components"] = Mock()
sys.modules["homeassistant.components.sensor"] = sensor
sys.modules["homeassistant.helpers"] = Mock()
sys.modules["homeassistant.helpers.entity"] = entity
sys.modules["homeassistant.helpers.entity_platform"] = entity_platform
sys.modules["homeassistant.helpers.update_coordinator"] = update_coordinator
sys.modules["homeassistant.helpers.selector"] = Mock()
sys.modules["homeassistant.helpers.device_registry"] = Mock()
sys.modules["homeassistant.util"] = Mock()
sys.modules["homeassistant.util.dt"] = dt_util
