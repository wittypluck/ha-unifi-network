from dataclasses import dataclass
from .api_client.models import ClientOverview, ClientDetails

@dataclass
class UnifiClient:
    """Represents a Unifi client with its overview and details."""

    overview: ClientOverview
    details: ClientDetails | None

    @property
    def name(self) -> str | None:
        """Return the client name."""
        return getattr(self.overview, "name", None)

    @property
    def ip(self) -> str | None:
        """Return the client IP address."""
        return getattr(self.overview, "ip_address", None)

    @property
    def mac(self) -> str | None:
        """Return the MAC address for this client.

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
                if mac:
                    return mac
        return None
