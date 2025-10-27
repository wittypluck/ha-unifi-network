from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.guest_authorization_details_authorization_method import GuestAuthorizationDetailsAuthorizationMethod
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.guest_authorization_usage_details import GuestAuthorizationUsageDetails





T = TypeVar("T", bound="GuestAuthorizationDetails")



@_attrs_define
class GuestAuthorizationDetails:
    """ 
        Attributes:
            authorized_at (datetime.datetime): Timestamp when the guest has been authorized
            authorization_method (GuestAuthorizationDetailsAuthorizationMethod): Guest authorization method (API, Voucher
                etc)
            expires_at (datetime.datetime): Timestamp when the guest will get automatically unauthorized
            data_usage_limit_m_bytes (Union[Unset, int]): (Optional) data usage limit in megabytes Example: 1024.
            rx_rate_limit_kbps (Union[Unset, int]): (Optional) download rate limit in kilobits per second Example: 1000.
            tx_rate_limit_kbps (Union[Unset, int]): (Optional) upload rate limit in kilobits per second Example: 1000.
            usage (Union[Unset, GuestAuthorizationUsageDetails]):
     """

    authorized_at: datetime.datetime
    authorization_method: GuestAuthorizationDetailsAuthorizationMethod
    expires_at: datetime.datetime
    data_usage_limit_m_bytes: Union[Unset, int] = UNSET
    rx_rate_limit_kbps: Union[Unset, int] = UNSET
    tx_rate_limit_kbps: Union[Unset, int] = UNSET
    usage: Union[Unset, 'GuestAuthorizationUsageDetails'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.guest_authorization_usage_details import GuestAuthorizationUsageDetails
        authorized_at = self.authorized_at.isoformat()

        authorization_method = self.authorization_method.value

        expires_at = self.expires_at.isoformat()

        data_usage_limit_m_bytes = self.data_usage_limit_m_bytes

        rx_rate_limit_kbps = self.rx_rate_limit_kbps

        tx_rate_limit_kbps = self.tx_rate_limit_kbps

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "authorizedAt": authorized_at,
            "authorizationMethod": authorization_method,
            "expiresAt": expires_at,
        })
        if data_usage_limit_m_bytes is not UNSET:
            field_dict["dataUsageLimitMBytes"] = data_usage_limit_m_bytes
        if rx_rate_limit_kbps is not UNSET:
            field_dict["rxRateLimitKbps"] = rx_rate_limit_kbps
        if tx_rate_limit_kbps is not UNSET:
            field_dict["txRateLimitKbps"] = tx_rate_limit_kbps
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guest_authorization_usage_details import GuestAuthorizationUsageDetails
        d = dict(src_dict)
        authorized_at = isoparse(d.pop("authorizedAt"))




        authorization_method = GuestAuthorizationDetailsAuthorizationMethod(d.pop("authorizationMethod"))




        expires_at = isoparse(d.pop("expiresAt"))




        data_usage_limit_m_bytes = d.pop("dataUsageLimitMBytes", UNSET)

        rx_rate_limit_kbps = d.pop("rxRateLimitKbps", UNSET)

        tx_rate_limit_kbps = d.pop("txRateLimitKbps", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, GuestAuthorizationUsageDetails]
        if isinstance(_usage,  Unset):
            usage = UNSET
        else:
            usage = GuestAuthorizationUsageDetails.from_dict(_usage)




        guest_authorization_details = cls(
            authorized_at=authorized_at,
            authorization_method=authorization_method,
            expires_at=expires_at,
            data_usage_limit_m_bytes=data_usage_limit_m_bytes,
            rx_rate_limit_kbps=rx_rate_limit_kbps,
            tx_rate_limit_kbps=tx_rate_limit_kbps,
            usage=usage,
        )


        guest_authorization_details.additional_properties = d
        return guest_authorization_details

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
