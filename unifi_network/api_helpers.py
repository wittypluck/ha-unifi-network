"""Helper utilities for UniFi API client operations."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from http import HTTPStatus
from typing import Any, TypeVar

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


async def fetch_all_pages(
    fetch_func: Callable[..., Awaitable[Any]], page_size: int = 100, **kwargs: Any
) -> list[T]:
    """
    Fetch all items from a paginated API endpoint.

    Args:
        fetch_func: The asyncio_detailed function from the API client
        page_size: Number of items to fetch per page (default: 100)
        **kwargs: Additional arguments to pass to the fetch function

    Returns:
        A list of all items across all pages

    Example:
        items = await fetch_all_pages(
            get_connected_client_overview_page.asyncio_detailed,
            client=client,
            site_id=site_id
        )
    """
    all_items = []
    offset = 0

    while True:
        response = await fetch_func(offset=offset, limit=page_size, **kwargs)

        if response is None or response.status_code != HTTPStatus.OK:
            raise ValueError(
                f"API returned status {getattr(response, 'status_code', None)}"
            )

        if not response.parsed:
            raise ValueError("No parsed response from API")

        page_data = getattr(response.parsed, "data", None) or []
        all_items.extend(page_data)

        # Check if we've fetched all items
        total_count = getattr(response.parsed, "total_count", 0)
        if offset + len(page_data) >= total_count:
            break

        offset += page_size

    _LOGGER.debug(
        "Fetched %d items across %d pages",
        len(all_items),
        (len(all_items) + page_size - 1) // page_size,
    )
    return all_items
