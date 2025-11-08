from dataclasses import dataclass

from .api_client.models import DeviceDetails, DeviceOverview, LatestStatisticsForADevice
from .api_client.types import Unset


@dataclass
class UnifiDevice:
    """Represents a Unifi device with its overview, statistics, and details."""

    overview: DeviceOverview
    latest_statistics: LatestStatisticsForADevice | None
    details: DeviceDetails | None

    @property
    def id(self) -> str:
        """Return the device ID as a string."""
        return str(self.overview.id)

    @property
    def name(self) -> str | None:
        """Return the device name."""
        name = getattr(self.overview, "name", None)
        if name is not None and isinstance(name, Unset):
            return None
        return name

    @property
    def ip(self) -> str | None:
        """Return the device IP address, or None if unset."""
        ip = getattr(self.overview, "ip_address", None)
        if ip is not None and isinstance(ip, Unset):
            return None
        return ip

    @property
    def mac(self) -> str | None:
        """Return the device MAC address, or None if unset."""
        mac = getattr(self.overview, "mac_address", None)
        if mac is not None and isinstance(mac, Unset):
            return None
        return mac
