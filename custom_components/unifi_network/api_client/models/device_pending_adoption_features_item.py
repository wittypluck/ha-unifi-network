from enum import Enum


class DevicePendingAdoptionFeaturesItem(str, Enum):
    ACCESSPOINT = "accessPoint"
    GATEWAY = "gateway"
    SWITCHING = "switching"

    def __str__(self) -> str:
        return str(self.value)
