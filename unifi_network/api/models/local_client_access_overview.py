from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="LocalClientAccessOverview")



@_attrs_define
class LocalClientAccessOverview:
    """ Represents the type of network access and/or any applicable authorization status the client is using.

    - **Wired clients** may have direct access without additional authorization.
    - **Wireless clients** can be connected via a protected network or an open network
      that may require additional authorization (e.g., a guest portal).
    - **VPN clients** may have different authorization mechanisms.

    Currently, the only two supported access types are `GUEST` (used for wired and wireless guest clients)
    and `DEFAULT` (a placeholder, which might be refined in the future releases, used for all other clients).

    Filtering is possible by `access.type`, for example `access.type.eq('GUEST')` to list guest clients.

        Attributes:
            type_ (str):
     """

    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        local_client_access_overview = cls(
            type_=type_,
        )


        local_client_access_overview.additional_properties = d
        return local_client_access_overview

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
