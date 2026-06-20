from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.integration_derived_site_to_site_tunnel_metadata_source import (
    IntegrationDerivedSiteToSiteTunnelMetadataSource,
)


T = TypeVar("T", bound="IntegrationDerivedSiteToSiteTunnelMetadata")


@_attrs_define
class IntegrationDerivedSiteToSiteTunnelMetadata:
    """
    Attributes:
        origin (str):
        source (IntegrationDerivedSiteToSiteTunnelMetadataSource):
    """

    origin: str
    source: IntegrationDerivedSiteToSiteTunnelMetadataSource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        origin = self.origin

        source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "origin": origin,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        origin = d.pop("origin")

        source = IntegrationDerivedSiteToSiteTunnelMetadataSource(d.pop("source"))

        integration_derived_site_to_site_tunnel_metadata = cls(
            origin=origin,
            source=source,
        )

        integration_derived_site_to_site_tunnel_metadata.additional_properties = d
        return integration_derived_site_to_site_tunnel_metadata

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
