from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="HotspotVoucherCreationRequest")


@_attrs_define
class HotspotVoucherCreationRequest:
    """
    Attributes:
        name (str): Voucher note, duplicated across all generated vouchers
        time_limit_minutes (int): How long (in minutes) the voucher will provide access to the network since
            authorization of the first guest.
            Subsequently connected guests, if allowed, will share the same expiration time.
        count (Union[Unset, int]): Number of vouchers to generate Default: 1.
        authorized_guest_limit (Union[Unset, int]): (Optional) limit for how many different guests can use the same
            voucher to authorize network access Example: 1.
        data_usage_limit_m_bytes (Union[Unset, int]): (Optional) data usage limit in megabytes
        rx_rate_limit_kbps (Union[Unset, int]): (Optional) download rate limit in kilobits per second
        tx_rate_limit_kbps (Union[Unset, int]): (Optional) upload rate limit in kilobits per second
    """

    name: str
    time_limit_minutes: int
    count: Union[Unset, int] = 1
    authorized_guest_limit: Union[Unset, int] = UNSET
    data_usage_limit_m_bytes: Union[Unset, int] = UNSET
    rx_rate_limit_kbps: Union[Unset, int] = UNSET
    tx_rate_limit_kbps: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        time_limit_minutes = self.time_limit_minutes

        count = self.count

        authorized_guest_limit = self.authorized_guest_limit

        data_usage_limit_m_bytes = self.data_usage_limit_m_bytes

        rx_rate_limit_kbps = self.rx_rate_limit_kbps

        tx_rate_limit_kbps = self.tx_rate_limit_kbps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "timeLimitMinutes": time_limit_minutes,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if authorized_guest_limit is not UNSET:
            field_dict["authorizedGuestLimit"] = authorized_guest_limit
        if data_usage_limit_m_bytes is not UNSET:
            field_dict["dataUsageLimitMBytes"] = data_usage_limit_m_bytes
        if rx_rate_limit_kbps is not UNSET:
            field_dict["rxRateLimitKbps"] = rx_rate_limit_kbps
        if tx_rate_limit_kbps is not UNSET:
            field_dict["txRateLimitKbps"] = tx_rate_limit_kbps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        time_limit_minutes = d.pop("timeLimitMinutes")

        count = d.pop("count", UNSET)

        authorized_guest_limit = d.pop("authorizedGuestLimit", UNSET)

        data_usage_limit_m_bytes = d.pop("dataUsageLimitMBytes", UNSET)

        rx_rate_limit_kbps = d.pop("rxRateLimitKbps", UNSET)

        tx_rate_limit_kbps = d.pop("txRateLimitKbps", UNSET)

        hotspot_voucher_creation_request = cls(
            name=name,
            time_limit_minutes=time_limit_minutes,
            count=count,
            authorized_guest_limit=authorized_guest_limit,
            data_usage_limit_m_bytes=data_usage_limit_m_bytes,
            rx_rate_limit_kbps=rx_rate_limit_kbps,
            tx_rate_limit_kbps=tx_rate_limit_kbps,
        )

        hotspot_voucher_creation_request.additional_properties = d
        return hotspot_voucher_creation_request

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
