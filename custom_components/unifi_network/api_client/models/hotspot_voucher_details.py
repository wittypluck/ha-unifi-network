from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime


T = TypeVar("T", bound="HotspotVoucherDetails")


@_attrs_define
class HotspotVoucherDetails:
    """
    Attributes:
        id (UUID):
        created_at (datetime.datetime):
        name (str): Voucher note, may contain duplicate values across multiple vouchers Example: hotel-guest.
        code (str): Secret code to active the voucher using the Hotspot portal Example: 4861409510.
        authorized_guest_count (int): For how many guests the voucher has been used to authorize network access
        expired (bool): Whether the voucher has been expired and can no longer be used to authorize network access
        time_limit_minutes (int): How long (in minutes) the voucher will provide access to the network since
            authorization of the first guest.
            Subsequently connected guests, if allowed, will share the same expiration time. Example: 1440.
        authorized_guest_limit (Union[Unset, int]): (Optional) limit for how many different guests can use the same
            voucher to authorize network access Example: 1.
        activated_at (Union[Unset, datetime.datetime]): (Optional) timestamp when the voucher has been activated
            (authorization time of the first guest)
        expires_at (Union[Unset, datetime.datetime]): (Optional) timestamp when the voucher will become expired. All
            guests using the voucher will be unauthorized from network access
        data_usage_limit_m_bytes (Union[Unset, int]): (Optional) data usage limit in megabytes Example: 1024.
        rx_rate_limit_kbps (Union[Unset, int]): (Optional) download rate limit in kilobits per second Example: 1000.
        tx_rate_limit_kbps (Union[Unset, int]): (Optional) upload rate limit in kilobits per second Example: 1000.
    """

    id: UUID
    created_at: datetime.datetime
    name: str
    code: str
    authorized_guest_count: int
    expired: bool
    time_limit_minutes: int
    authorized_guest_limit: Union[Unset, int] = UNSET
    activated_at: Union[Unset, datetime.datetime] = UNSET
    expires_at: Union[Unset, datetime.datetime] = UNSET
    data_usage_limit_m_bytes: Union[Unset, int] = UNSET
    rx_rate_limit_kbps: Union[Unset, int] = UNSET
    tx_rate_limit_kbps: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        created_at = self.created_at.isoformat()

        name = self.name

        code = self.code

        authorized_guest_count = self.authorized_guest_count

        expired = self.expired

        time_limit_minutes = self.time_limit_minutes

        authorized_guest_limit = self.authorized_guest_limit

        activated_at: Union[Unset, str] = UNSET
        if not isinstance(self.activated_at, Unset):
            activated_at = self.activated_at.isoformat()

        expires_at: Union[Unset, str] = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        data_usage_limit_m_bytes = self.data_usage_limit_m_bytes

        rx_rate_limit_kbps = self.rx_rate_limit_kbps

        tx_rate_limit_kbps = self.tx_rate_limit_kbps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "createdAt": created_at,
                "name": name,
                "code": code,
                "authorizedGuestCount": authorized_guest_count,
                "expired": expired,
                "timeLimitMinutes": time_limit_minutes,
            }
        )
        if authorized_guest_limit is not UNSET:
            field_dict["authorizedGuestLimit"] = authorized_guest_limit
        if activated_at is not UNSET:
            field_dict["activatedAt"] = activated_at
        if expires_at is not UNSET:
            field_dict["expiresAt"] = expires_at
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
        id = UUID(d.pop("id"))

        created_at = isoparse(d.pop("createdAt"))

        name = d.pop("name")

        code = d.pop("code")

        authorized_guest_count = d.pop("authorizedGuestCount")

        expired = d.pop("expired")

        time_limit_minutes = d.pop("timeLimitMinutes")

        authorized_guest_limit = d.pop("authorizedGuestLimit", UNSET)

        _activated_at = d.pop("activatedAt", UNSET)
        activated_at: Union[Unset, datetime.datetime]
        if isinstance(_activated_at, Unset):
            activated_at = UNSET
        else:
            activated_at = isoparse(_activated_at)

        _expires_at = d.pop("expiresAt", UNSET)
        expires_at: Union[Unset, datetime.datetime]
        if isinstance(_expires_at, Unset):
            expires_at = UNSET
        else:
            expires_at = isoparse(_expires_at)

        data_usage_limit_m_bytes = d.pop("dataUsageLimitMBytes", UNSET)

        rx_rate_limit_kbps = d.pop("rxRateLimitKbps", UNSET)

        tx_rate_limit_kbps = d.pop("txRateLimitKbps", UNSET)

        hotspot_voucher_details = cls(
            id=id,
            created_at=created_at,
            name=name,
            code=code,
            authorized_guest_count=authorized_guest_count,
            expired=expired,
            time_limit_minutes=time_limit_minutes,
            authorized_guest_limit=authorized_guest_limit,
            activated_at=activated_at,
            expires_at=expires_at,
            data_usage_limit_m_bytes=data_usage_limit_m_bytes,
            rx_rate_limit_kbps=rx_rate_limit_kbps,
            tx_rate_limit_kbps=tx_rate_limit_kbps,
        )

        hotspot_voucher_details.additional_properties = d
        return hotspot_voucher_details

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
