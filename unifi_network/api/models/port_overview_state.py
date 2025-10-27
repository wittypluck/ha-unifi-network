from enum import Enum

class PortOverviewState(str, Enum):
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"
    UP = "UP"

    def __str__(self) -> str:
        return str(self.value)
