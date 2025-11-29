from enum import Enum


class GuestAuthorizationDetailsAuthorizationMethod(str, Enum):
    API = "API"
    OTHER = "OTHER"
    VOUCHER = "VOUCHER"

    def __str__(self) -> str:
        return str(self.value)
