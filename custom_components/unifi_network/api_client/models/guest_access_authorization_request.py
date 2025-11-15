from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GuestAccessAuthorizationRequest")


@_attrs_define
class GuestAccessAuthorizationRequest:
    """Authorizes network access to a guest client. Client must be a guest.
    This action cancels existing active authorization (if exists), creates a new one with new limits
    and resets guest traffic counters.

        Attributes:
            action (str):
            time_limit_minutes (Union[Unset, int]): (Optional) how long (in minutes) the guest will be authorized to access
                the network.
                If not specified, the default limit is used from the site settings
            data_usage_limit_m_bytes (Union[Unset, int]): (Optional) data usage limit in megabytes
            rx_rate_limit_kbps (Union[Unset, int]): (Optional) download rate limit in kilobits per second
            tx_rate_limit_kbps (Union[Unset, int]): (Optional) upload rate limit in kilobits per second
    """

    action: str
    time_limit_minutes: Union[Unset, int] = UNSET
    data_usage_limit_m_bytes: Union[Unset, int] = UNSET
    rx_rate_limit_kbps: Union[Unset, int] = UNSET
    tx_rate_limit_kbps: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        time_limit_minutes = self.time_limit_minutes

        data_usage_limit_m_bytes = self.data_usage_limit_m_bytes

        rx_rate_limit_kbps = self.rx_rate_limit_kbps

        tx_rate_limit_kbps = self.tx_rate_limit_kbps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )
        if time_limit_minutes is not UNSET:
            field_dict["timeLimitMinutes"] = time_limit_minutes
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
        action = d.pop("action")

        time_limit_minutes = d.pop("timeLimitMinutes", UNSET)

        data_usage_limit_m_bytes = d.pop("dataUsageLimitMBytes", UNSET)

        rx_rate_limit_kbps = d.pop("rxRateLimitKbps", UNSET)

        tx_rate_limit_kbps = d.pop("txRateLimitKbps", UNSET)

        guest_access_authorization_request = cls(
            action=action,
            time_limit_minutes=time_limit_minutes,
            data_usage_limit_m_bytes=data_usage_limit_m_bytes,
            rx_rate_limit_kbps=rx_rate_limit_kbps,
            tx_rate_limit_kbps=tx_rate_limit_kbps,
        )

        guest_access_authorization_request.additional_properties = d
        return guest_access_authorization_request

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
