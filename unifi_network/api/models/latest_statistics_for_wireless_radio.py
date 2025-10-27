from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="LatestStatisticsForWirelessRadio")



@_attrs_define
class LatestStatisticsForWirelessRadio:
    """ 
        Attributes:
            frequency_g_hz (float):
            tx_retries_pct (Union[Unset, float]):
     """

    frequency_g_hz: float
    tx_retries_pct: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        frequency_g_hz = self.frequency_g_hz

        tx_retries_pct = self.tx_retries_pct


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "frequencyGHz": frequency_g_hz,
        })
        if tx_retries_pct is not UNSET:
            field_dict["txRetriesPct"] = tx_retries_pct

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        frequency_g_hz = d.pop("frequencyGHz")

        tx_retries_pct = d.pop("txRetriesPct", UNSET)

        latest_statistics_for_wireless_radio = cls(
            frequency_g_hz=frequency_g_hz,
            tx_retries_pct=tx_retries_pct,
        )


        latest_statistics_for_wireless_radio.additional_properties = d
        return latest_statistics_for_wireless_radio

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
