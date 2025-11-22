from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.device_pending_adoption_features_item import (
    DevicePendingAdoptionFeaturesItem,
)
from ..models.device_pending_adoption_state import DevicePendingAdoptionState
from typing import cast
from typing import Union


T = TypeVar("T", bound="DevicePendingAdoption")


@_attrs_define
class DevicePendingAdoption:
    """
    Attributes:
        mac_address (str):  Example: 94:2a:6f:26:c6:ca.
        ip_address (str):  Example: 192.168.1.55.
        model (str):  Example: UHDIW.
        state (DevicePendingAdoptionState):
        supported (bool):
        firmware_updatable (bool):
        features (list[DevicePendingAdoptionFeaturesItem]):
        firmware_version (Union[Unset, str]):  Example: 6.6.55.
    """

    mac_address: str
    ip_address: str
    model: str
    state: DevicePendingAdoptionState
    supported: bool
    firmware_updatable: bool
    features: list[DevicePendingAdoptionFeaturesItem]
    firmware_version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mac_address = self.mac_address

        ip_address = self.ip_address

        model = self.model

        state = self.state.value

        supported = self.supported

        firmware_updatable = self.firmware_updatable

        features = []
        for features_item_data in self.features:
            features_item = features_item_data.value
            features.append(features_item)

        firmware_version = self.firmware_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "macAddress": mac_address,
                "ipAddress": ip_address,
                "model": model,
                "state": state,
                "supported": supported,
                "firmwareUpdatable": firmware_updatable,
                "features": features,
            }
        )
        if firmware_version is not UNSET:
            field_dict["firmwareVersion"] = firmware_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mac_address = d.pop("macAddress")

        ip_address = d.pop("ipAddress")

        model = d.pop("model")

        state = DevicePendingAdoptionState(d.pop("state"))

        supported = d.pop("supported")

        firmware_updatable = d.pop("firmwareUpdatable")

        features = []
        _features = d.pop("features")
        for features_item_data in _features:
            features_item = DevicePendingAdoptionFeaturesItem(features_item_data)

            features.append(features_item)

        firmware_version = d.pop("firmwareVersion", UNSET)

        device_pending_adoption = cls(
            mac_address=mac_address,
            ip_address=ip_address,
            model=model,
            state=state,
            supported=supported,
            firmware_updatable=firmware_updatable,
            features=features,
            firmware_version=firmware_version,
        )

        device_pending_adoption.additional_properties = d
        return device_pending_adoption

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
