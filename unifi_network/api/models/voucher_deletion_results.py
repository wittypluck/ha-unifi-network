from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VoucherDeletionResults")



@_attrs_define
class VoucherDeletionResults:
    """ 
        Attributes:
            vouchers_deleted (Union[Unset, int]):
     """

    vouchers_deleted: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        vouchers_deleted = self.vouchers_deleted


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if vouchers_deleted is not UNSET:
            field_dict["vouchersDeleted"] = vouchers_deleted

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vouchers_deleted = d.pop("vouchersDeleted", UNSET)

        voucher_deletion_results = cls(
            vouchers_deleted=vouchers_deleted,
        )


        voucher_deletion_results.additional_properties = d
        return voucher_deletion_results

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
