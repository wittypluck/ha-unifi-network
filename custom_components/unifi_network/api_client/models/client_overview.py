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


T = TypeVar("T", bound="ClientOverview")


@_attrs_define
class ClientOverview:
    """
    Attributes:
        id (UUID):
        name (str):
        access (Any):  Example: {'type': 'DEFAULT'}.
        type_ (str):
        connected_at (Union[Unset, datetime.datetime]):
        ip_address (Union[Unset, str]):
    """

    id: UUID
    name: str
    access: Any
    type_: str
    connected_at: Union[Unset, datetime.datetime] = UNSET
    ip_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        access = self.access

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
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        access = d.pop("access")

        type_ = d.pop("type")

        _connected_at = d.pop("connectedAt", UNSET)
        connected_at: Union[Unset, datetime.datetime]
        if isinstance(_connected_at, Unset):
            connected_at = UNSET
        else:
            connected_at = isoparse(_connected_at)

        ip_address = d.pop("ipAddress", UNSET)

        client_overview = cls(
            id=id,
            name=name,
            access=access,
            type_=type_,
            connected_at=connected_at,
            ip_address=ip_address,
        )

        client_overview.additional_properties = d
        return client_overview

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
