from enum import Enum


class IntegrationDerivedSiteToSiteTunnelMetadataSource(str, Enum):
    SDWAN = "SDWAN"

    def __str__(self) -> str:
        return str(self.value)
