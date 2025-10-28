from dataclasses import dataclass

from .api_client.models import ClientDetails, ClientOverview
from .api_client.types import Unset


@dataclass
class UnifiClient:
    """Represents a Unifi client with its overview and details."""

    overview: ClientOverview
    details: ClientDetails | None

    @property
    def name(self) -> str | None:
        """Return the client name, or None if unset."""
        name = getattr(self.overview, "name", None)
        if name is not None and isinstance(name, Unset):
            return None
        return name

    @property
    def ip(self) -> str | None:
        """Return the client IP address, or None if unset."""
        ip = getattr(self.overview, "ip_address", None)
        if ip is not None and isinstance(ip, Unset):
            return None
        return ip

    @property
    def mac(self) -> str | None:
        """Return the MAC address for this client, or None if unset.

        The OpenAPI models keep unrecognized fields in `additional_properties`.
        UniFi currently exposes the MAC under the key "macAddress".
        """
        # Prefer value from overview, then fall back to details if present
        for src in (self.overview, self.details):
            if not src:
                continue
            additional = getattr(src, "additional_properties", None)
            if isinstance(additional, dict):
                mac = additional.get("macAddress")
                if mac is not None and isinstance(mac, Unset):
                    return None
                if mac:
                    return mac
        return None
