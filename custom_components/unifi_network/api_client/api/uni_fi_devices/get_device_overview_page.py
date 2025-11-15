from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.device_overview_page import DeviceOverviewPage
from ...types import Unset
from uuid import UUID


def _get_kwargs(
    site_id: UUID,
    *,
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/devices".format(
            site_id=site_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeviceOverviewPage]:
    if response.status_code == 200:
        response_200 = DeviceOverviewPage.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeviceOverviewPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
) -> Response[DeviceOverviewPage]:
    """List Devices

     Retrieve a paginated list of all adopted devices on a site, including basic device information.

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeviceOverviewPage]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
) -> Optional[DeviceOverviewPage]:
    """List Devices

     Retrieve a paginated list of all adopted devices on a site, including basic device information.

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeviceOverviewPage
    """

    return sync_detailed(
        site_id=site_id,
        client=client,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
) -> Response[DeviceOverviewPage]:
    """List Devices

     Retrieve a paginated list of all adopted devices on a site, including basic device information.

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeviceOverviewPage]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
) -> Optional[DeviceOverviewPage]:
    """List Devices

     Retrieve a paginated list of all adopted devices on a site, including basic device information.

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeviceOverviewPage
    """

    return (
        await asyncio_detailed(
            site_id=site_id,
            client=client,
            offset=offset,
            limit=limit,
        )
    ).parsed
