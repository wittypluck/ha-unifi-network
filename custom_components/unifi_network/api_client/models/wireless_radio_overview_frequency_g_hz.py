from enum import Enum


class WirelessRadioOverviewFrequencyGHz(str, Enum):
    VALUE_0 = "2.4"
    VALUE_1 = "5"
    VALUE_2 = "6"
    VALUE_3 = "60"

    def __str__(self) -> str:
        return str(self.value)
