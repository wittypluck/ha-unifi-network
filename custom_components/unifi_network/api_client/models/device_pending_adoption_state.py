from enum import Enum


class DevicePendingAdoptionState(str, Enum):
    ADOPTING = "ADOPTING"
    CONNECTION_INTERRUPTED = "CONNECTION_INTERRUPTED"
    DELETING = "DELETING"
    GETTING_READY = "GETTING_READY"
    ISOLATED = "ISOLATED"
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    PENDING_ADOPTION = "PENDING_ADOPTION"
    UPDATING = "UPDATING"

    def __str__(self) -> str:
        return str(self.value)
