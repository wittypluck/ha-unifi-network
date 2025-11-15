from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hotspot_voucher_details import HotspotVoucherDetails
from uuid import UUID


def _get_kwargs(
    site_id: UUID,
    voucher_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}".format(
            site_id=site_id,
            voucher_id=voucher_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HotspotVoucherDetails]:
    if response.status_code == 200:
        response_200 = HotspotVoucherDetails.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HotspotVoucherDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_id: UUID,
    voucher_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[HotspotVoucherDetails]:
    """Get Voucher Details

     Retrieve details of a specific Hotspot voucher.

    Args:
        site_id (UUID):
        voucher_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotspotVoucherDetails]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        voucher_id=voucher_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    site_id: UUID,
    voucher_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[HotspotVoucherDetails]:
    """Get Voucher Details

     Retrieve details of a specific Hotspot voucher.

    Args:
        site_id (UUID):
        voucher_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotspotVoucherDetails
    """

    return sync_detailed(
        site_id=site_id,
        voucher_id=voucher_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    site_id: UUID,
    voucher_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[HotspotVoucherDetails]:
    """Get Voucher Details

     Retrieve details of a specific Hotspot voucher.

    Args:
        site_id (UUID):
        voucher_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotspotVoucherDetails]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        voucher_id=voucher_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    site_id: UUID,
    voucher_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[HotspotVoucherDetails]:
    """Get Voucher Details

     Retrieve details of a specific Hotspot voucher.

    Args:
        site_id (UUID):
        voucher_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotspotVoucherDetails
    """

    return (
        await asyncio_detailed(
            site_id=site_id,
            voucher_id=voucher_id,
            client=client,
        )
    ).parsed
