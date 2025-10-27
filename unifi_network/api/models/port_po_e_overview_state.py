from enum import Enum

class PortPoEOverviewState(str, Enum):
    DOWN = "DOWN"
    LIMITED = "LIMITED"
    UNKNOWN = "UNKNOWN"
    UP = "UP"

    def __str__(self) -> str:
        return str(self.value)
