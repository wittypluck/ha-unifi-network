from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="DeviceFeatures")


@_attrs_define
class DeviceFeatures:
    """
    Attributes:
        switching (Union[Unset, Any]):
        access_point (Union[Unset, Any]):
    """

    switching: Union[Unset, Any] = UNSET
    access_point: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        switching = self.switching

        access_point = self.access_point

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if switching is not UNSET:
            field_dict["switching"] = switching
        if access_point is not UNSET:
            field_dict["accessPoint"] = access_point

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        switching = d.pop("switching", UNSET)

        access_point = d.pop("accessPoint", UNSET)

        device_features = cls(
            switching=switching,
            access_point=access_point,
        )

        device_features.additional_properties = d
        return device_features

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
