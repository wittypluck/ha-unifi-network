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

if TYPE_CHECKING:
    from ..models.vpn_client_access_overview import VPNClientAccessOverview


T = TypeVar("T", bound="VPNClientConnectionOverview")


@_attrs_define
class VPNClientConnectionOverview:
    """
    Attributes:
        id (UUID):
        name (str):
        access (VPNClientAccessOverview): Represents the type of network access and/or any applicable authorization
            status the client is using.

            - **Wired clients** may have direct access without additional authorization.
            - **Wireless clients** can be connected via a protected network or an open network
              that may require additional authorization (e.g., a guest portal).
            - **VPN clients** may have different authorization mechanisms.

            Currently, the only two supported access types are `GUEST` (used for wired and wireless guest clients)
            and `DEFAULT` (a placeholder, which might be refined in the future releases, used for all other clients).

            Filtering is possible by `access.type`, for example `access.type.eq('GUEST')` to list guest clients. Example:
            {'type': 'DEFAULT'}.
        type_ (str):
        connected_at (Union[Unset, datetime.datetime]):
        ip_address (Union[Unset, str]):
    """

    id: UUID
    name: str
    access: "VPNClientAccessOverview"
    type_: str
    connected_at: Union[Unset, datetime.datetime] = UNSET
    ip_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.vpn_client_access_overview import VPNClientAccessOverview

        id = str(self.id)

        name = self.name

        access = self.access.to_dict()

        type_ = self.type_

        connected_at: Union[Unset, str] = UNSET
        if not isinstance(self.connected_at, Unset):
            connected_at = self.connected_at.isoformat()

        ip_address = self.ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "access": access,
                "type": type_,
            }
        )
        if connected_at is not UNSET:
            field_dict["connectedAt"] = connected_at
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vpn_client_access_overview import VPNClientAccessOverview

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        access = VPNClientAccessOverview.from_dict(d.pop("access"))

        type_ = d.pop("type")

        _connected_at = d.pop("connectedAt", UNSET)
        connected_at: Union[Unset, datetime.datetime]
        if isinstance(_connected_at, Unset):
            connected_at = UNSET
        else:
            connected_at = isoparse(_connected_at)

        ip_address = d.pop("ipAddress", UNSET)

        vpn_client_connection_overview = cls(
            id=id,
            name=name,
            access=access,
            type_=type_,
            connected_at=connected_at,
            ip_address=ip_address,
        )

        vpn_client_connection_overview.additional_properties = d
        return vpn_client_connection_overview

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
