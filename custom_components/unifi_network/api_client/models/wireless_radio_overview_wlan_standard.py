from enum import Enum


class WirelessRadioOverviewWlanStandard(str, Enum):
    VALUE_0 = "802.11a"
    VALUE_1 = "802.11b"
    VALUE_2 = "802.11g"
    VALUE_3 = "802.11n"
    VALUE_4 = "802.11ac"
    VALUE_5 = "802.11ax"
    VALUE_6 = "802.11be"

    def __str__(self) -> str:
        return str(self.value)
