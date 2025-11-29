from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.guest_authorization_details import GuestAuthorizationDetails


T = TypeVar("T", bound="GuestAccessDetails")


@_attrs_define
class GuestAccessDetails:
    """
    Attributes:
        type_ (str):
        authorized (bool):
        authorization (Union[Unset, GuestAuthorizationDetails]):
    """

    type_: str
    authorized: bool
    authorization: Union[Unset, "GuestAuthorizationDetails"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.guest_authorization_details import GuestAuthorizationDetails

        type_ = self.type_

        authorized = self.authorized

        authorization: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.authorization, Unset):
            authorization = self.authorization.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "authorized": authorized,
            }
        )
        if authorization is not UNSET:
            field_dict["authorization"] = authorization

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guest_authorization_details import GuestAuthorizationDetails

        d = dict(src_dict)
        type_ = d.pop("type")

        authorized = d.pop("authorized")

        _authorization = d.pop("authorization", UNSET)
        authorization: Union[Unset, GuestAuthorizationDetails]
        if isinstance(_authorization, Unset):
            authorization = UNSET
        else:
            authorization = GuestAuthorizationDetails.from_dict(_authorization)

        guest_access_details = cls(
            type_=type_,
            authorized=authorized,
            authorization=authorization,
        )

        guest_access_details.additional_properties = d
        return guest_access_details

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
