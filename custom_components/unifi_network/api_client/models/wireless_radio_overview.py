from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.wireless_radio_overview_frequency_g_hz import (
    WirelessRadioOverviewFrequencyGHz,
)
from ..models.wireless_radio_overview_wlan_standard import (
    WirelessRadioOverviewWlanStandard,
)
from typing import Union


T = TypeVar("T", bound="WirelessRadioOverview")


@_attrs_define
class WirelessRadioOverview:
    """
    Attributes:
        wlan_standard (WirelessRadioOverviewWlanStandard):
        frequency_g_hz (WirelessRadioOverviewFrequencyGHz):
        channel_width_m_hz (int):  Example: 40.
        channel (Union[Unset, int]):  Example: 36.
    """

    wlan_standard: WirelessRadioOverviewWlanStandard
    frequency_g_hz: WirelessRadioOverviewFrequencyGHz
    channel_width_m_hz: int
    channel: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        wlan_standard = self.wlan_standard.value

        frequency_g_hz = self.frequency_g_hz.value

        channel_width_m_hz = self.channel_width_m_hz

        channel = self.channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "wlanStandard": wlan_standard,
                "frequencyGHz": frequency_g_hz,
                "channelWidthMHz": channel_width_m_hz,
            }
        )
        if channel is not UNSET:
            field_dict["channel"] = channel

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        wlan_standard = WirelessRadioOverviewWlanStandard(d.pop("wlanStandard"))

        frequency_g_hz = WirelessRadioOverviewFrequencyGHz(d.pop("frequencyGHz"))

        channel_width_m_hz = d.pop("channelWidthMHz")

        channel = d.pop("channel", UNSET)

        wireless_radio_overview = cls(
            wlan_standard=wlan_standard,
            frequency_g_hz=frequency_g_hz,
            channel_width_m_hz=channel_width_m_hz,
            channel=channel,
        )

        wireless_radio_overview.additional_properties = d
        return wireless_radio_overview

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
