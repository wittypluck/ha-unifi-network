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
    from ..models.teleport_client_access_overview import TeleportClientAccessOverview


T = TypeVar("T", bound="TeleportClientConnectionOverview")


@_attrs_define
class TeleportClientConnectionOverview:
    """
    Attributes:
        type_ (str):
        id (UUID):
        name (str):
        access (TeleportClientAccessOverview): Represents the type of network access and/or any applicable authorization
            status the client is using.

            - **Wired clients** may have direct access without additional authorization.
            - **Wireless clients** can be connected via a protected network or an open network
              that may require additional authorization (e.g., a guest portal).
            - **VPN clients** may have different authorization mechanisms.

            Currently, the only two supported access types are `GUEST` (used for wired and wireless guest clients)
            and `DEFAULT` (a placeholder, which might be refined in the future releases, used for all other clients).

            Filtering is possible by `access.type`, for example `access.type.eq('GUEST')` to list guest clients. Example:
            {'type': 'DEFAULT'}.
        connected_at (Union[Unset, datetime.datetime]):
        ip_address (Union[Unset, str]):
    """

    type_: str
    id: UUID
    name: str
    access: "TeleportClientAccessOverview"
    connected_at: Union[Unset, datetime.datetime] = UNSET
    ip_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.teleport_client_access_overview import (
            TeleportClientAccessOverview,
        )

        type_ = self.type_

        id = str(self.id)

        name = self.name

        access = self.access.to_dict()

        connected_at: Union[Unset, str] = UNSET
        if not isinstance(self.connected_at, Unset):
            connected_at = self.connected_at.isoformat()

        ip_address = self.ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "id": id,
                "name": name,
                "access": access,
            }
        )
        if connected_at is not UNSET:
            field_dict["connectedAt"] = connected_at
        if ip_address is not UNSET:
            field_dict["ipAddress"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.teleport_client_access_overview import (
            TeleportClientAccessOverview,
        )

        d = dict(src_dict)
        type_ = d.pop("type")

        id = UUID(d.pop("id"))

        name = d.pop("name")

        access = TeleportClientAccessOverview.from_dict(d.pop("access"))

        _connected_at = d.pop("connectedAt", UNSET)
        connected_at: Union[Unset, datetime.datetime]
        if isinstance(_connected_at, Unset):
            connected_at = UNSET
        else:
            connected_at = isoparse(_connected_at)

        ip_address = d.pop("ipAddress", UNSET)

        teleport_client_connection_overview = cls(
            type_=type_,
            id=id,
            name=name,
            access=access,
            connected_at=connected_at,
            ip_address=ip_address,
        )

        teleport_client_connection_overview.additional_properties = d
        return teleport_client_connection_overview

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
