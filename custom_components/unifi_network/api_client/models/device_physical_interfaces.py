from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.port_overview import PortOverview
    from ..models.wireless_radio_overview import WirelessRadioOverview


T = TypeVar("T", bound="DevicePhysicalInterfaces")


@_attrs_define
class DevicePhysicalInterfaces:
    """
    Attributes:
        ports (Union[Unset, list['PortOverview']]):
        radios (Union[Unset, list['WirelessRadioOverview']]):
    """

    ports: Union[Unset, list["PortOverview"]] = UNSET
    radios: Union[Unset, list["WirelessRadioOverview"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.port_overview import PortOverview
        from ..models.wireless_radio_overview import WirelessRadioOverview

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                ports.append(ports_item)

        radios: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.radios, Unset):
            radios = []
            for radios_item_data in self.radios:
                radios_item = radios_item_data.to_dict()
                radios.append(radios_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ports is not UNSET:
            field_dict["ports"] = ports
        if radios is not UNSET:
            field_dict["radios"] = radios

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.port_overview import PortOverview
        from ..models.wireless_radio_overview import WirelessRadioOverview

        d = dict(src_dict)
        ports = []
        _ports = d.pop("ports", UNSET)
        for ports_item_data in _ports or []:
            ports_item = PortOverview.from_dict(ports_item_data)

            ports.append(ports_item)

        radios = []
        _radios = d.pop("radios", UNSET)
        for radios_item_data in _radios or []:
            radios_item = WirelessRadioOverview.from_dict(radios_item_data)

            radios.append(radios_item)

        device_physical_interfaces = cls(
            ports=ports,
            radios=radios,
        )

        device_physical_interfaces.additional_properties = d
        return device_physical_interfaces

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
