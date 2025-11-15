from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.port_po_e_overview_standard import PortPoEOverviewStandard
from ..models.port_po_e_overview_state import PortPoEOverviewState
from ..models.port_po_e_overview_type import PortPoEOverviewType


T = TypeVar("T", bound="PortPoEOverview")


@_attrs_define
class PortPoEOverview:
    """
    Attributes:
        standard (PortPoEOverviewStandard):  Example: 802.3bt.
        type_ (PortPoEOverviewType):  Example: 3.
        enabled (bool): Whether the PoE feature is enabled on the port
        state (PortPoEOverviewState): Whether the port currently supplies power to the (connected) device.
    """

    standard: PortPoEOverviewStandard
    type_: PortPoEOverviewType
    enabled: bool
    state: PortPoEOverviewState
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        standard = self.standard.value

        type_ = self.type_.value

        enabled = self.enabled

        state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "standard": standard,
                "type": type_,
                "enabled": enabled,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        standard = PortPoEOverviewStandard(d.pop("standard"))

        type_ = PortPoEOverviewType(d.pop("type"))

        enabled = d.pop("enabled")

        state = PortPoEOverviewState(d.pop("state"))

        port_po_e_overview = cls(
            standard=standard,
            type_=type_,
            enabled=enabled,
            state=state,
        )

        port_po_e_overview.additional_properties = d
        return port_po_e_overview

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
