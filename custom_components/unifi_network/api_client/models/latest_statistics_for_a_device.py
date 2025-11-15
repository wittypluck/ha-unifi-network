from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.latest_statistics_for_a_device_uplink_interface import (
        LatestStatisticsForADeviceUplinkInterface,
    )
    from ..models.latest_statistics_for_device_interfaces import (
        LatestStatisticsForDeviceInterfaces,
    )


T = TypeVar("T", bound="LatestStatisticsForADevice")


@_attrs_define
class LatestStatisticsForADevice:
    """
    Attributes:
        interfaces (LatestStatisticsForDeviceInterfaces):
        uptime_sec (Union[Unset, int]):
        last_heartbeat_at (Union[Unset, datetime.datetime]):
        next_heartbeat_at (Union[Unset, datetime.datetime]):
        load_average_1_min (Union[Unset, float]):
        load_average_5_min (Union[Unset, float]):
        load_average_15_min (Union[Unset, float]):
        cpu_utilization_pct (Union[Unset, float]):
        memory_utilization_pct (Union[Unset, float]):
        uplink (Union[Unset, LatestStatisticsForADeviceUplinkInterface]):
    """

    interfaces: "LatestStatisticsForDeviceInterfaces"
    uptime_sec: Union[Unset, int] = UNSET
    last_heartbeat_at: Union[Unset, datetime.datetime] = UNSET
    next_heartbeat_at: Union[Unset, datetime.datetime] = UNSET
    load_average_1_min: Union[Unset, float] = UNSET
    load_average_5_min: Union[Unset, float] = UNSET
    load_average_15_min: Union[Unset, float] = UNSET
    cpu_utilization_pct: Union[Unset, float] = UNSET
    memory_utilization_pct: Union[Unset, float] = UNSET
    uplink: Union[Unset, "LatestStatisticsForADeviceUplinkInterface"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.latest_statistics_for_a_device_uplink_interface import (
            LatestStatisticsForADeviceUplinkInterface,
        )
        from ..models.latest_statistics_for_device_interfaces import (
            LatestStatisticsForDeviceInterfaces,
        )

        interfaces = self.interfaces.to_dict()

        uptime_sec = self.uptime_sec

        last_heartbeat_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_heartbeat_at, Unset):
            last_heartbeat_at = self.last_heartbeat_at.isoformat()

        next_heartbeat_at: Union[Unset, str] = UNSET
        if not isinstance(self.next_heartbeat_at, Unset):
            next_heartbeat_at = self.next_heartbeat_at.isoformat()

        load_average_1_min = self.load_average_1_min

        load_average_5_min = self.load_average_5_min

        load_average_15_min = self.load_average_15_min

        cpu_utilization_pct = self.cpu_utilization_pct

        memory_utilization_pct = self.memory_utilization_pct

        uplink: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.uplink, Unset):
            uplink = self.uplink.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "interfaces": interfaces,
            }
        )
        if uptime_sec is not UNSET:
            field_dict["uptimeSec"] = uptime_sec
        if last_heartbeat_at is not UNSET:
            field_dict["lastHeartbeatAt"] = last_heartbeat_at
        if next_heartbeat_at is not UNSET:
            field_dict["nextHeartbeatAt"] = next_heartbeat_at
        if load_average_1_min is not UNSET:
            field_dict["loadAverage1Min"] = load_average_1_min
        if load_average_5_min is not UNSET:
            field_dict["loadAverage5Min"] = load_average_5_min
        if load_average_15_min is not UNSET:
            field_dict["loadAverage15Min"] = load_average_15_min
        if cpu_utilization_pct is not UNSET:
            field_dict["cpuUtilizationPct"] = cpu_utilization_pct
        if memory_utilization_pct is not UNSET:
            field_dict["memoryUtilizationPct"] = memory_utilization_pct
        if uplink is not UNSET:
            field_dict["uplink"] = uplink

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.latest_statistics_for_a_device_uplink_interface import (
            LatestStatisticsForADeviceUplinkInterface,
        )
        from ..models.latest_statistics_for_device_interfaces import (
            LatestStatisticsForDeviceInterfaces,
        )

        d = dict(src_dict)
        interfaces = LatestStatisticsForDeviceInterfaces.from_dict(d.pop("interfaces"))

        uptime_sec = d.pop("uptimeSec", UNSET)

        _last_heartbeat_at = d.pop("lastHeartbeatAt", UNSET)
        last_heartbeat_at: Union[Unset, datetime.datetime]
        if isinstance(_last_heartbeat_at, Unset):
            last_heartbeat_at = UNSET
        else:
            last_heartbeat_at = isoparse(_last_heartbeat_at)

        _next_heartbeat_at = d.pop("nextHeartbeatAt", UNSET)
        next_heartbeat_at: Union[Unset, datetime.datetime]
        if isinstance(_next_heartbeat_at, Unset):
            next_heartbeat_at = UNSET
        else:
            next_heartbeat_at = isoparse(_next_heartbeat_at)

        load_average_1_min = d.pop("loadAverage1Min", UNSET)

        load_average_5_min = d.pop("loadAverage5Min", UNSET)

        load_average_15_min = d.pop("loadAverage15Min", UNSET)

        cpu_utilization_pct = d.pop("cpuUtilizationPct", UNSET)

        memory_utilization_pct = d.pop("memoryUtilizationPct", UNSET)

        _uplink = d.pop("uplink", UNSET)
        uplink: Union[Unset, LatestStatisticsForADeviceUplinkInterface]
        if isinstance(_uplink, Unset):
            uplink = UNSET
        else:
            uplink = LatestStatisticsForADeviceUplinkInterface.from_dict(_uplink)

        latest_statistics_for_a_device = cls(
            interfaces=interfaces,
            uptime_sec=uptime_sec,
            last_heartbeat_at=last_heartbeat_at,
            next_heartbeat_at=next_heartbeat_at,
            load_average_1_min=load_average_1_min,
            load_average_5_min=load_average_5_min,
            load_average_15_min=load_average_15_min,
            cpu_utilization_pct=cpu_utilization_pct,
            memory_utilization_pct=memory_utilization_pct,
            uplink=uplink,
        )

        latest_statistics_for_a_device.additional_properties = d
        return latest_statistics_for_a_device

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
