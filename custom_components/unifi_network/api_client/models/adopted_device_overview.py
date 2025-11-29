from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.adopted_device_overview_features_item import (
    AdoptedDeviceOverviewFeaturesItem,
)
from ..models.adopted_device_overview_interfaces_item import (
    AdoptedDeviceOverviewInterfacesItem,
)
from ..models.adopted_device_overview_state import AdoptedDeviceOverviewState
from typing import cast
from typing import Union
from uuid import UUID


T = TypeVar("T", bound="AdoptedDeviceOverview")


@_attrs_define
class AdoptedDeviceOverview:
    """
    Attributes:
        id (UUID):
        mac_address (str):  Example: 94:2a:6f:26:c6:ca.
        ip_address (str):  Example: 192.168.1.55.
        name (str):  Example: IW HD.
        model (str):  Example: UHDIW.
        state (AdoptedDeviceOverviewState):
        supported (bool):
        firmware_updatable (bool):
        features (list[AdoptedDeviceOverviewFeaturesItem]):
        interfaces (list[AdoptedDeviceOverviewInterfacesItem]):
        firmware_version (Union[Unset, str]):  Example: 6.6.55.
    """

    id: UUID
    mac_address: str
    ip_address: str
    name: str
    model: str
    state: AdoptedDeviceOverviewState
    supported: bool
    firmware_updatable: bool
    features: list[AdoptedDeviceOverviewFeaturesItem]
    interfaces: list[AdoptedDeviceOverviewInterfacesItem]
    firmware_version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        mac_address = self.mac_address

        ip_address = self.ip_address

        name = self.name

        model = self.model

        state = self.state.value

        supported = self.supported

        firmware_updatable = self.firmware_updatable

        features = []
        for features_item_data in self.features:
            features_item = features_item_data.value
            features.append(features_item)

        interfaces = []
        for interfaces_item_data in self.interfaces:
            interfaces_item = interfaces_item_data.value
            interfaces.append(interfaces_item)

        firmware_version = self.firmware_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "macAddress": mac_address,
                "ipAddress": ip_address,
                "name": name,
                "model": model,
                "state": state,
                "supported": supported,
                "firmwareUpdatable": firmware_updatable,
                "features": features,
                "interfaces": interfaces,
            }
        )
        if firmware_version is not UNSET:
            field_dict["firmwareVersion"] = firmware_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        mac_address = d.pop("macAddress")

        ip_address = d.pop("ipAddress")

        name = d.pop("name")

        model = d.pop("model")

        state = AdoptedDeviceOverviewState(d.pop("state"))

        supported = d.pop("supported")

        firmware_updatable = d.pop("firmwareUpdatable")

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = AdoptedDeviceOverviewFeaturesItem(features_item_data)

            features.append(features_item)

        interfaces = []
        _interfaces = d.pop("interfaces")
        for interfaces_item_data in _interfaces:
            interfaces_item = AdoptedDeviceOverviewInterfacesItem(interfaces_item_data)

            interfaces.append(interfaces_item)

        firmware_version = d.pop("firmwareVersion", UNSET)

        adopted_device_overview = cls(
            id=id,
            mac_address=mac_address,
            ip_address=ip_address,
            name=name,
            model=model,
            state=state,
            supported=supported,
            firmware_updatable=firmware_updatable,
            features=features,
            interfaces=interfaces,
            firmware_version=firmware_version,
        )

        adopted_device_overview.additional_properties = d
        return adopted_device_overview

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
