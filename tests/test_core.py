"""Test the core module."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

from unifi_network.core import UnifiNetworkCore


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = Mock()
    hass.data = {}
    return hass


@pytest.fixture
def mock_httpx_client():
    """Create a mock httpx AsyncClient."""
    return AsyncMock()


@patch("unifi_network.core.create_async_httpx_client")
@patch("unifi_network.core.Client")
@patch("unifi_network.core.UnifiDeviceCoordinator")
@patch("unifi_network.core.UnifiClientCoordinator")
@pytest.mark.asyncio
async def test_init_creates_client_and_async_init_refreshes_coordinators(
    mock_client_coordinator,
    mock_device_coordinator,
    mock_client_class,
    mock_create_client,
    mock_hass,
):
    """Test that __init__ creates client and async_init refreshes coordinators."""
    mock_client = Mock()
    mock_httpx_client = Mock()
    mock_httpx_client.headers = Mock()
    mock_client_class.return_value = mock_client
    mock_create_client.return_value = mock_httpx_client

    mock_device_coordinator_instance = AsyncMock()
    mock_client_coordinator_instance = AsyncMock()
    mock_device_coordinator.return_value = mock_device_coordinator_instance
    mock_client_coordinator.return_value = mock_client_coordinator_instance

    core = UnifiNetworkCore(
        hass=mock_hass,
        base_url="https://unifi.example.com",
        site_id="default",
        api_key="test-key",
        enable_devices=True,
        enable_clients=True,
        verify_ssl=True,
    )

    # Verify create_async_httpx_client was called with correct parameters during __init__
    mock_create_client.assert_called_once_with(
        mock_hass,
        verify_ssl=True,
        base_url="https://unifi.example.com",
    )

    # Verify headers were added to the httpx client during __init__
    mock_httpx_client.headers.update.assert_called_once_with({"X-API-Key": "test-key"})

    # Verify Client was called with correct parameters during __init__
    mock_client_class.assert_called_once_with(base_url="https://unifi.example.com")

    # Verify set_async_httpx_client was called during __init__
    mock_client.set_async_httpx_client.assert_called_once_with(mock_httpx_client)

    # Verify the client was created during __init__
    assert core.client == mock_client

    await core.async_init()

    # Verify coordinators were refreshed
    mock_device_coordinator_instance.async_config_entry_first_refresh.assert_called_once()
    mock_client_coordinator_instance.async_config_entry_first_refresh.assert_called_once()


@patch("unifi_network.core.create_async_httpx_client")
@patch("unifi_network.core.Client")
@patch("unifi_network.core.UnifiDeviceCoordinator")
@patch("unifi_network.core.UnifiClientCoordinator")
@pytest.mark.asyncio
async def test_init_respects_verify_ssl_false(
    mock_client_coordinator,
    mock_device_coordinator,
    mock_client_class,
    mock_create_client,
    mock_hass,
):
    """Test that __init__ respects verify_ssl=False setting."""
    # Setup mocks
    mock_client = Mock()
    mock_httpx_client = Mock()
    mock_httpx_client.headers = Mock()
    mock_client_class.return_value = mock_client
    mock_create_client.return_value = mock_httpx_client
    mock_device_coordinator_instance = AsyncMock()
    mock_client_coordinator_instance = AsyncMock()
    mock_device_coordinator.return_value = mock_device_coordinator_instance
    mock_client_coordinator.return_value = mock_client_coordinator_instance

    # Create core instance with verify_ssl=False
    core = UnifiNetworkCore(
        hass=mock_hass,
        base_url="https://unifi.example.com",
        site_id="default",
        api_key="test-key",
        enable_devices=True,
        enable_clients=True,
        verify_ssl=False,
    )

    # Verify create_async_httpx_client was called with verify_ssl=False during __init__
    mock_create_client.assert_called_once_with(
        mock_hass,
        verify_ssl=False,
        base_url="https://unifi.example.com",
    )

    # Verify headers were added to the httpx client during __init__
    mock_httpx_client.headers.update.assert_called_once_with({"X-API-Key": "test-key"})

    # Verify Client was called with correct parameters during __init__
    mock_client_class.assert_called_once_with(base_url="https://unifi.example.com")

    # Verify set_async_httpx_client was called during __init__
    mock_client.set_async_httpx_client.assert_called_once_with(mock_httpx_client)

    # Verify the client was created during __init__
    assert core.client == mock_client

    # Call async_init
    await core.async_init()

    # Verify coordinators were refreshed
    mock_device_coordinator_instance.async_config_entry_first_refresh.assert_called_once()
    mock_client_coordinator_instance.async_config_entry_first_refresh.assert_called_once()


@patch("unifi_network.core.create_async_httpx_client")
@patch("unifi_network.core.Client")
@pytest.mark.asyncio
async def test_init_without_coordinators(
    mock_client_class,
    mock_create_client,
    mock_hass,
):
    """Test that __init__ creates client when coordinators are disabled."""
    # Setup mocks
    mock_client = Mock()
    mock_httpx_client = Mock()
    mock_httpx_client.headers = Mock()
    mock_client_class.return_value = mock_client
    mock_create_client.return_value = mock_httpx_client

    # Create core instance with both coordinators disabled
    core = UnifiNetworkCore(
        hass=mock_hass,
        base_url="https://unifi.example.com",
        site_id="default",
        api_key="test-key",
        enable_devices=False,
        enable_clients=False,
        verify_ssl=True,
    )

    # Verify create_async_httpx_client was called with correct parameters during __init__
    mock_create_client.assert_called_once_with(
        mock_hass,
        verify_ssl=True,
        base_url="https://unifi.example.com",
    )

    # Verify headers were added to the httpx client during __init__
    mock_httpx_client.headers.update.assert_called_once_with({"X-API-Key": "test-key"})

    # Verify Client was called with correct parameters during __init__
    mock_client_class.assert_called_once_with(base_url="https://unifi.example.com")

    # Verify set_async_httpx_client was called during __init__
    mock_client.set_async_httpx_client.assert_called_once_with(mock_httpx_client)

    # Verify the client was created during __init__ but coordinators are None
    assert core.client == mock_client
    assert core.device_coordinator is None
    assert core.client_coordinator is None

    # Call async_init
    await core.async_init()

    # Since coordinators are disabled, no refresh calls should be made
    # This completes successfully without any coordinator operations


@patch("unifi_network.core.create_async_httpx_client")
@patch("unifi_network.core.Client")
@pytest.mark.asyncio
async def test_init_without_api_key(
    mock_client_class,
    mock_create_client,
    mock_hass,
):
    """Test that __init__ works when api_key is None."""
    # Setup mocks
    mock_client = Mock()
    mock_httpx_client = Mock()
    mock_httpx_client.headers = Mock()
    mock_client_class.return_value = mock_client
    mock_create_client.return_value = mock_httpx_client

    # Create core instance without api_key
    core = UnifiNetworkCore(
        hass=mock_hass,
        base_url="https://unifi.example.com",
        site_id="default",
        api_key=None,
        enable_devices=False,
        enable_clients=False,
        verify_ssl=True,
    )

    # Verify create_async_httpx_client was called with correct parameters during __init__
    mock_create_client.assert_called_once_with(
        mock_hass,
        verify_ssl=True,
        base_url="https://unifi.example.com",
    )

    # Verify headers were NOT updated when api_key is None
    mock_httpx_client.headers.update.assert_not_called()

    # Verify Client was called with correct parameters during __init__
    mock_client_class.assert_called_once_with(base_url="https://unifi.example.com")

    # Verify set_async_httpx_client was called during __init__
    mock_client.set_async_httpx_client.assert_called_once_with(mock_httpx_client)

    # Verify the client was created during __init__
    assert core.client == mock_client
    assert core.device_coordinator is None
    assert core.client_coordinator is None

    # Call async_init
    await core.async_init()

    # Since coordinators are disabled, no refresh calls should be made
    # This completes successfully without any coordinator operations
