from dataclasses import dataclass
from .api_client.models import DeviceOverview, LatestStatisticsForADevice

@dataclass
class UnifiDevice:
    """Represents a Unifi device with its overview and statistics."""

    overview: DeviceOverview
    latest_statistics: LatestStatisticsForADevice | None

    @property
    def name(self) -> str | None:
        """Return the device name."""
        return getattr(self.overview, "name", None)

    @property
    def ip(self) -> str | None:
        """Return the device IP address."""
        return getattr(self.overview, "ip_address", None)

    @property
    def mac(self) -> str | None:
        """Return the device MAC address."""
        return getattr(self.overview, "mac_address", None)
