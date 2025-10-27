from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.device_overview import DeviceOverview





T = TypeVar("T", bound="DeviceOverviewPage")



@_attrs_define
class DeviceOverviewPage:
    """ 
        Attributes:
            offset (int):
            limit (int):  Example: 25.
            count (int):  Example: 10.
            total_count (int):  Example: 1000.
            data (list['DeviceOverview']):
     """

    offset: int
    limit: int
    count: int
    total_count: int
    data: list['DeviceOverview']
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.device_overview import DeviceOverview
        offset = self.offset

        limit = self.limit

        count = self.count

        total_count = self.total_count

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "offset": offset,
            "limit": limit,
            "count": count,
            "totalCount": total_count,
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.device_overview import DeviceOverview
        d = dict(src_dict)
        offset = d.pop("offset")

        limit = d.pop("limit")

        count = d.pop("count")

        total_count = d.pop("totalCount")

        data = []
        _data = d.pop("data")
        for data_item_data in (_data):
            data_item = DeviceOverview.from_dict(data_item_data)



            data.append(data_item)


        device_overview_page = cls(
            offset=offset,
            limit=limit,
            count=count,
            total_count=total_count,
            data=data,
        )


        device_overview_page.additional_properties = d
        return device_overview_page

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
