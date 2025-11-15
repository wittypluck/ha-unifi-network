from enum import Enum


class DeviceOverviewInterfacesItem(str, Enum):
    PORTS = "ports"
    RADIOS = "radios"

    def __str__(self) -> str:
        return str(self.value)
