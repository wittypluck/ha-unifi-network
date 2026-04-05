from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="IntegrationDeviceAdoptionRequestDto")


@_attrs_define
class IntegrationDeviceAdoptionRequestDto:
    """
    Attributes:
        mac_address (str):
        ignore_device_limit (bool):
    """

    mac_address: str
    ignore_device_limit: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mac_address = self.mac_address

        ignore_device_limit = self.ignore_device_limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "macAddress": mac_address,
                "ignoreDeviceLimit": ignore_device_limit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mac_address = d.pop("macAddress")

        ignore_device_limit = d.pop("ignoreDeviceLimit")

        integration_device_adoption_request_dto = cls(
            mac_address=mac_address,
            ignore_device_limit=ignore_device_limit,
        )

        integration_device_adoption_request_dto.additional_properties = d
        return integration_device_adoption_request_dto

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
