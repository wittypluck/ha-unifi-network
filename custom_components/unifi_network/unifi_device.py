from dataclasses import dataclass

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.entity import DeviceInfo

from .api_client.models import DeviceDetails, DeviceOverview, LatestStatisticsForADevice
from .api_client.types import Unset
from .const import ATTR_MANUFACTURER, DOMAIN


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

    @property
    def firmware_version(self) -> str | None:
        """Return the device firmware version, or None if not available."""
        if not self.details:
            return None
        firmware_version = getattr(self.details, "firmware_version", None)
        if firmware_version is not None and isinstance(firmware_version, Unset):
            return None
        return firmware_version

    @property
    def firmware_updatable(self) -> bool:
        """Return whether the device firmware can be updated."""
        if not self.details:
            return False
        return getattr(self.details, "firmware_updatable", False)

    @property
    def device_info(self) -> DeviceInfo:
        """Return DeviceInfo for this UniFi device with manufacturer set."""
        model = getattr(self.overview, "model", None)
        identifiers = {(DOMAIN, self.id)}
        connections = {(CONNECTION_NETWORK_MAC, self.mac)} if self.mac else set()

        return DeviceInfo(
            identifiers=identifiers,
            name=self.name,
            model=model,
            manufacturer=ATTR_MANUFACTURER,
            connections=connections,
        )
