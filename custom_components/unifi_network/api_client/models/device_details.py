from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.device_details_state import DeviceDetailsState
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
    from ..models.device_physical_interfaces import DevicePhysicalInterfaces
    from ..models.device_uplink_interface_overview import DeviceUplinkInterfaceOverview
    from ..models.device_features import DeviceFeatures


T = TypeVar("T", bound="DeviceDetails")


@_attrs_define
class DeviceDetails:
    """
    Attributes:
        id (UUID):
        name (str):  Example: IW HD.
        model (str):  Example: UHDIW.
        supported (bool):
        mac_address (str):  Example: 94:2a:6f:26:c6:ca.
        ip_address (str):  Example: 192.168.1.55.
        state (DeviceDetailsState):
        firmware_updatable (bool):
        configuration_id (str):  Example: 7596498d2f367dc2.
        features (DeviceFeatures):
        interfaces (DevicePhysicalInterfaces):
        firmware_version (Union[Unset, str]):  Example: 6.6.55.
        adopted_at (Union[Unset, datetime.datetime]):
        provisioned_at (Union[Unset, datetime.datetime]):
        uplink (Union[Unset, DeviceUplinkInterfaceOverview]): Uplink interface is device's connection to the parent
            device in the network topology
    """

    id: UUID
    name: str
    model: str
    supported: bool
    mac_address: str
    ip_address: str
    state: DeviceDetailsState
    firmware_updatable: bool
    configuration_id: str
    features: "DeviceFeatures"
    interfaces: "DevicePhysicalInterfaces"
    firmware_version: Union[Unset, str] = UNSET
    adopted_at: Union[Unset, datetime.datetime] = UNSET
    provisioned_at: Union[Unset, datetime.datetime] = UNSET
    uplink: Union[Unset, "DeviceUplinkInterfaceOverview"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_physical_interfaces import DevicePhysicalInterfaces
        from ..models.device_uplink_interface_overview import (
            DeviceUplinkInterfaceOverview,
        )
        from ..models.device_features import DeviceFeatures

        id = str(self.id)

        name = self.name

        model = self.model

        supported = self.supported

        mac_address = self.mac_address

        ip_address = self.ip_address

        state = self.state.value

        firmware_updatable = self.firmware_updatable

        configuration_id = self.configuration_id

        features = self.features.to_dict()

        interfaces = self.interfaces.to_dict()

        firmware_version = self.firmware_version

        adopted_at: Union[Unset, str] = UNSET
        if not isinstance(self.adopted_at, Unset):
            adopted_at = self.adopted_at.isoformat()

        provisioned_at: Union[Unset, str] = UNSET
        if not isinstance(self.provisioned_at, Unset):
            provisioned_at = self.provisioned_at.isoformat()

        uplink: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.uplink, Unset):
            uplink = self.uplink.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "model": model,
                "supported": supported,
                "macAddress": mac_address,
                "ipAddress": ip_address,
                "state": state,
                "firmwareUpdatable": firmware_updatable,
                "configurationId": configuration_id,
                "features": features,
                "interfaces": interfaces,
            }
        )
        if firmware_version is not UNSET:
            field_dict["firmwareVersion"] = firmware_version
        if adopted_at is not UNSET:
            field_dict["adoptedAt"] = adopted_at
        if provisioned_at is not UNSET:
            field_dict["provisionedAt"] = provisioned_at
        if uplink is not UNSET:
            field_dict["uplink"] = uplink

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.device_physical_interfaces import DevicePhysicalInterfaces
        from ..models.device_uplink_interface_overview import (
            DeviceUplinkInterfaceOverview,
        )
        from ..models.device_features import DeviceFeatures

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        model = d.pop("model")

        supported = d.pop("supported")

        mac_address = d.pop("macAddress")

        ip_address = d.pop("ipAddress")

        state = DeviceDetailsState(d.pop("state"))

        firmware_updatable = d.pop("firmwareUpdatable")

        configuration_id = d.pop("configurationId")

        features = DeviceFeatures.from_dict(d.pop("features"))

        interfaces = DevicePhysicalInterfaces.from_dict(d.pop("interfaces"))

        firmware_version = d.pop("firmwareVersion", UNSET)

        _adopted_at = d.pop("adoptedAt", UNSET)
        adopted_at: Union[Unset, datetime.datetime]
        if isinstance(_adopted_at, Unset):
            adopted_at = UNSET
        else:
            adopted_at = isoparse(_adopted_at)

        _provisioned_at = d.pop("provisionedAt", UNSET)
        provisioned_at: Union[Unset, datetime.datetime]
        if isinstance(_provisioned_at, Unset):
            provisioned_at = UNSET
        else:
            provisioned_at = isoparse(_provisioned_at)

        _uplink = d.pop("uplink", UNSET)
        uplink: Union[Unset, DeviceUplinkInterfaceOverview]
        if isinstance(_uplink, Unset):
            uplink = UNSET
        else:
            uplink = DeviceUplinkInterfaceOverview.from_dict(_uplink)

        device_details = cls(
            id=id,
            name=name,
            model=model,
            supported=supported,
            mac_address=mac_address,
            ip_address=ip_address,
            state=state,
            firmware_updatable=firmware_updatable,
            configuration_id=configuration_id,
            features=features,
            interfaces=interfaces,
            firmware_version=firmware_version,
            adopted_at=adopted_at,
            provisioned_at=provisioned_at,
            uplink=uplink,
        )

        device_details.additional_properties = d
        return device_details

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
