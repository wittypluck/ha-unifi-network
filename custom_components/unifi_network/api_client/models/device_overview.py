from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.device_overview_features_item import DeviceOverviewFeaturesItem
from ..models.device_overview_interfaces_item import DeviceOverviewInterfacesItem
from ..models.device_overview_state import DeviceOverviewState
from typing import cast
from uuid import UUID


T = TypeVar("T", bound="DeviceOverview")


@_attrs_define
class DeviceOverview:
    """
    Attributes:
        id (UUID):
        name (str):  Example: IW HD.
        model (str):  Example: UHDIW.
        mac_address (str):  Example: 94:2a:6f:26:c6:ca.
        ip_address (str):  Example: 192.168.1.55.
        state (DeviceOverviewState):
        features (list[DeviceOverviewFeaturesItem]):
        interfaces (list[DeviceOverviewInterfacesItem]):
    """

    id: UUID
    name: str
    model: str
    mac_address: str
    ip_address: str
    state: DeviceOverviewState
    features: list[DeviceOverviewFeaturesItem]
    interfaces: list[DeviceOverviewInterfacesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        model = self.model

        mac_address = self.mac_address

        ip_address = self.ip_address

        state = self.state.value

        features = []
        for features_item_data in self.features:
            features_item = features_item_data.value
            features.append(features_item)

        interfaces = []
        for interfaces_item_data in self.interfaces:
            interfaces_item = interfaces_item_data.value
            interfaces.append(interfaces_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "model": model,
                "macAddress": mac_address,
                "ipAddress": ip_address,
                "state": state,
                "features": features,
                "interfaces": interfaces,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        model = d.pop("model")

        mac_address = d.pop("macAddress")

        ip_address = d.pop("ipAddress")

        state = DeviceOverviewState(d.pop("state"))

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = DeviceOverviewFeaturesItem(features_item_data)

            features.append(features_item)

        interfaces = []
        _interfaces = d.pop("interfaces")
        for interfaces_item_data in _interfaces:
            interfaces_item = DeviceOverviewInterfacesItem(interfaces_item_data)

            interfaces.append(interfaces_item)

        device_overview = cls(
            id=id,
            name=name,
            model=model,
            mac_address=mac_address,
            ip_address=ip_address,
            state=state,
            features=features,
            interfaces=interfaces,
        )

        device_overview.additional_properties = d
        return device_overview

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
