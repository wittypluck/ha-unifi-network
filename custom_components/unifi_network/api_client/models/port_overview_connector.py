from enum import Enum


class PortOverviewConnector(str, Enum):
    QSFP28 = "QSFP28"
    RJ45 = "RJ45"
    SFP = "SFP"
    SFP28 = "SFP28"
    SFPPLUS = "SFPPLUS"

    def __str__(self) -> str:
        return str(self.value)
