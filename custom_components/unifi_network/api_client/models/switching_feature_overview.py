from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.integration_local_lag_local_dto import IntegrationLocalLagLocalDto


T = TypeVar("T", bound="SwitchingFeatureOverview")


@_attrs_define
class SwitchingFeatureOverview:
    """
    Attributes:
        lags (list['IntegrationLocalLagLocalDto']):
    """

    lags: list["IntegrationLocalLagLocalDto"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.integration_local_lag_local_dto import IntegrationLocalLagLocalDto

        lags = []
        for lags_item_data in self.lags:
            lags_item = lags_item_data.to_dict()
            lags.append(lags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lags": lags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_local_lag_local_dto import IntegrationLocalLagLocalDto

        d = dict(src_dict)
        lags = []
        _lags = d.pop("lags")
        for lags_item_data in _lags:
            lags_item = IntegrationLocalLagLocalDto.from_dict(lags_item_data)

            lags.append(lags_item)

        switching_feature_overview = cls(
            lags=lags,
        )

        switching_feature_overview.additional_properties = d
        return switching_feature_overview

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
