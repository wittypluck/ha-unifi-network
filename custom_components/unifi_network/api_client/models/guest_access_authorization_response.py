from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.guest_authorization_details import GuestAuthorizationDetails





T = TypeVar("T", bound="GuestAccessAuthorizationResponse")



@_attrs_define
class GuestAccessAuthorizationResponse:
    """ 
        Attributes:
            action (str):
            granted_authorization (GuestAuthorizationDetails):
            revoked_authorization (Union[Unset, GuestAuthorizationDetails]):
     """

    action: str
    granted_authorization: 'GuestAuthorizationDetails'
    revoked_authorization: Union[Unset, 'GuestAuthorizationDetails'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.guest_authorization_details import GuestAuthorizationDetails
        action = self.action

        granted_authorization = self.granted_authorization.to_dict()

        revoked_authorization: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.revoked_authorization, Unset):
            revoked_authorization = self.revoked_authorization.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
            "grantedAuthorization": granted_authorization,
        })
        if revoked_authorization is not UNSET:
            field_dict["revokedAuthorization"] = revoked_authorization

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.guest_authorization_details import GuestAuthorizationDetails
        d = dict(src_dict)
        action = d.pop("action")

        granted_authorization = GuestAuthorizationDetails.from_dict(d.pop("grantedAuthorization"))




        _revoked_authorization = d.pop("revokedAuthorization", UNSET)
        revoked_authorization: Union[Unset, GuestAuthorizationDetails]
        if isinstance(_revoked_authorization,  Unset):
            revoked_authorization = UNSET
        else:
            revoked_authorization = GuestAuthorizationDetails.from_dict(_revoked_authorization)




        guest_access_authorization_response = cls(
            action=action,
            granted_authorization=granted_authorization,
            revoked_authorization=revoked_authorization,
        )


        guest_access_authorization_response.additional_properties = d
        return guest_access_authorization_response

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
