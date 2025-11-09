from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="ErrorMessage")



@_attrs_define
class ErrorMessage:
    """ 
        Attributes:
            status_code (Union[Unset, int]):  Example: 400.
            status_name (Union[Unset, str]):  Example: UNAUTHORIZED.
            message (Union[Unset, str]):  Example: Missing credentials.
            timestamp (Union[Unset, datetime.datetime]):  Example: 2024-11-27T08:13:46.966Z.
            request_path (Union[Unset, str]):  Example: /integration/v1/sites/123.
            request_id (Union[Unset, UUID]): In case of Internal Server Error (core = 500), request ID can be used to track
                down the error in the server log Example: 3fa85f64-5717-4562-b3fc-2c963f66afa6.
     """

    status_code: Union[Unset, int] = UNSET
    status_name: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    request_path: Union[Unset, str] = UNSET
    request_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status_code = self.status_code

        status_name = self.status_name

        message = self.message

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        request_path = self.request_path

        request_id: Union[Unset, str] = UNSET
        if not isinstance(self.request_id, Unset):
            request_id = str(self.request_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if status_code is not UNSET:
            field_dict["statusCode"] = status_code
        if status_name is not UNSET:
            field_dict["statusName"] = status_name
        if message is not UNSET:
            field_dict["message"] = message
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if request_path is not UNSET:
            field_dict["requestPath"] = request_path
        if request_id is not UNSET:
            field_dict["requestId"] = request_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status_code = d.pop("statusCode", UNSET)

        status_name = d.pop("statusName", UNSET)

        message = d.pop("message", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp,  Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)




        request_path = d.pop("requestPath", UNSET)

        _request_id = d.pop("requestId", UNSET)
        request_id: Union[Unset, UUID]
        if isinstance(_request_id,  Unset):
            request_id = UNSET
        else:
            request_id = UUID(_request_id)




        error_message = cls(
            status_code=status_code,
            status_name=status_name,
            message=message,
            timestamp=timestamp,
            request_path=request_path,
            request_id=request_id,
        )


        error_message.additional_properties = d
        return error_message

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
