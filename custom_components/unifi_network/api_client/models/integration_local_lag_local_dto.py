from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
    from ..models.user_defined_entity_metadata import UserDefinedEntityMetadata


T = TypeVar("T", bound="IntegrationLocalLagLocalDto")


@_attrs_define
class IntegrationLocalLagLocalDto:
    """
    Attributes:
        id (UUID):
        port_idxs (list[int]):
        metadata (UserDefinedEntityMetadata):
    """

    id: UUID
    port_idxs: list[int]
    metadata: "UserDefinedEntityMetadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_defined_entity_metadata import UserDefinedEntityMetadata

        id = str(self.id)

        port_idxs = self.port_idxs

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "portIdxs": port_idxs,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_defined_entity_metadata import UserDefinedEntityMetadata

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        port_idxs = cast(list[int], d.pop("portIdxs"))

        metadata = UserDefinedEntityMetadata.from_dict(d.pop("metadata"))

        integration_local_lag_local_dto = cls(
            id=id,
            port_idxs=port_idxs,
            metadata=metadata,
        )

        integration_local_lag_local_dto.additional_properties = d
        return integration_local_lag_local_dto

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
