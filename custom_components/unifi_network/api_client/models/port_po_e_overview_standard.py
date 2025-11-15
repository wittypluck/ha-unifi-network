from enum import Enum


class PortPoEOverviewStandard(str, Enum):
    VALUE_0 = "802.3af"
    VALUE_1 = "802.3at"
    VALUE_2 = "802.3bt"

    def __str__(self) -> str:
        return str(self.value)
