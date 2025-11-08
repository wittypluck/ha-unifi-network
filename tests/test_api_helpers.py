"""Tests for API helper functionality."""

from __future__ import annotations

from http import HTTPStatus
from unittest.mock import AsyncMock, Mock

import pytest

# Import conftest to set up mocks
import tests.conftest  # noqa: F401
from unifi_network.api_helpers import fetch_all_pages


class MockResponse:
    """Mock HTTP response."""

    def __init__(self, status_code, parsed_data=None, total_count=0):
        self.status_code = status_code
        self.parsed = Mock() if parsed_data is not None else None
        if self.parsed:
            self.parsed.data = parsed_data
            self.parsed.total_count = total_count


class TestFetchAllPages:
    """Test the fetch_all_pages helper function."""

    async def test_single_page_success(self):
        """Test fetching a single page of data."""
        # Mock data
        mock_data = [{"id": "item1"}, {"id": "item2"}]
        mock_response = MockResponse(HTTPStatus.OK, mock_data, 2)

        # Mock function
        mock_fetch_func = AsyncMock(return_value=mock_response)

        result = await fetch_all_pages(mock_fetch_func, test_param="value")

        assert result == mock_data
        mock_fetch_func.assert_called_once_with(offset=0, limit=100, test_param="value")

    async def test_multiple_pages_success(self):
        """Test fetching multiple pages of data."""
        # Mock data for multiple pages
        page1_data = [{"id": "item1"}, {"id": "item2"}]
        page2_data = [{"id": "item3"}]

        page1_response = MockResponse(HTTPStatus.OK, page1_data, 3)
        page2_response = MockResponse(HTTPStatus.OK, page2_data, 3)

        # Mock function that returns different responses
        mock_fetch_func = AsyncMock(side_effect=[page1_response, page2_response])

        result = await fetch_all_pages(mock_fetch_func, page_size=2)

        assert result == page1_data + page2_data
        assert mock_fetch_func.call_count == 2
        mock_fetch_func.assert_any_call(offset=0, limit=2)
        mock_fetch_func.assert_any_call(offset=2, limit=2)

    async def test_empty_pages(self):
        """Test handling of empty pages."""
        mock_response = MockResponse(HTTPStatus.OK, [], 0)
        mock_fetch_func = AsyncMock(return_value=mock_response)

        result = await fetch_all_pages(mock_fetch_func)

        assert result == []
        mock_fetch_func.assert_called_once_with(offset=0, limit=100)

    async def test_http_error_response(self):
        """Test handling of HTTP error responses."""
        mock_response = MockResponse(HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_fetch_func = AsyncMock(return_value=mock_response)

        with pytest.raises(ValueError, match="API returned status 500"):
            await fetch_all_pages(mock_fetch_func)

    async def test_none_response(self):
        """Test handling of None response."""
        mock_fetch_func = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="API returned status None"):
            await fetch_all_pages(mock_fetch_func)

    async def test_no_parsed_response(self):
        """Test handling of response without parsed data."""
        mock_response = MockResponse(HTTPStatus.OK)
        mock_response.parsed = None
        mock_fetch_func = AsyncMock(return_value=mock_response)

        with pytest.raises(ValueError, match="No parsed response from API"):
            await fetch_all_pages(mock_fetch_func)

    async def test_missing_data_attribute(self):
        """Test handling of parsed response without data attribute."""
        mock_response = MockResponse(HTTPStatus.OK)
        mock_response.parsed = Mock()
        mock_response.parsed.total_count = 0
        # Don't set data attribute - getattr will return None
        del mock_response.parsed.data
        mock_fetch_func = AsyncMock(return_value=mock_response)

        result = await fetch_all_pages(mock_fetch_func)

        assert result == []

    async def test_custom_page_size(self):
        """Test using custom page size."""
        mock_data = [{"id": "item1"}]
        mock_response = MockResponse(HTTPStatus.OK, mock_data, 1)
        mock_fetch_func = AsyncMock(return_value=mock_response)

        result = await fetch_all_pages(mock_fetch_func, page_size=50)

        assert result == mock_data
        mock_fetch_func.assert_called_once_with(offset=0, limit=50)

    async def test_additional_kwargs(self):
        """Test passing additional keyword arguments."""
        mock_data = [{"id": "item1"}]
        mock_response = MockResponse(HTTPStatus.OK, mock_data, 1)
        mock_fetch_func = AsyncMock(return_value=mock_response)

        result = await fetch_all_pages(
            mock_fetch_func, site_id="test-site", client="test-client", extra_param=42
        )

        assert result == mock_data
        mock_fetch_func.assert_called_once_with(
            offset=0,
            limit=100,
            site_id="test-site",
            client="test-client",
            extra_param=42,
        )

    async def test_pagination_with_exact_page_boundary(self):
        """Test pagination when data exactly fits page boundaries."""
        # 2 pages, each with exactly 2 items
        page1_data = [{"id": "item1"}, {"id": "item2"}]
        page2_data = [{"id": "item3"}, {"id": "item4"}]

        page1_response = MockResponse(HTTPStatus.OK, page1_data, 4)
        page2_response = MockResponse(HTTPStatus.OK, page2_data, 4)

        mock_fetch_func = AsyncMock(side_effect=[page1_response, page2_response])

        result = await fetch_all_pages(mock_fetch_func, page_size=2)

        assert result == page1_data + page2_data
        assert mock_fetch_func.call_count == 2
