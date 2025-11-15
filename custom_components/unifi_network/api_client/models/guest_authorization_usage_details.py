from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="GuestAuthorizationUsageDetails")


@_attrs_define
class GuestAuthorizationUsageDetails:
    """
    Attributes:
        duration_sec (int):
        rx_bytes (int):
        tx_bytes (int):
        bytes_ (int):
    """

    duration_sec: int
    rx_bytes: int
    tx_bytes: int
    bytes_: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_sec = self.duration_sec

        rx_bytes = self.rx_bytes

        tx_bytes = self.tx_bytes

        bytes_ = self.bytes_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "durationSec": duration_sec,
                "rxBytes": rx_bytes,
                "txBytes": tx_bytes,
                "bytes": bytes_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration_sec = d.pop("durationSec")

        rx_bytes = d.pop("rxBytes")

        tx_bytes = d.pop("txBytes")

        bytes_ = d.pop("bytes")

        guest_authorization_usage_details = cls(
            duration_sec=duration_sec,
            rx_bytes=rx_bytes,
            tx_bytes=tx_bytes,
            bytes_=bytes_,
        )

        guest_authorization_usage_details.additional_properties = d
        return guest_authorization_usage_details

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
