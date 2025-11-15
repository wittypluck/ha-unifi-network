from enum import Enum


class DeviceOverviewFeaturesItem(str, Enum):
    ACCESSPOINT = "accessPoint"
    GATEWAY = "gateway"
    SWITCHING = "switching"

    def __str__(self) -> str:
        return str(self.value)
