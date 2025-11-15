from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.voucher_deletion_results import VoucherDeletionResults
from uuid import UUID


def _get_kwargs(
    site_id: UUID,
    *,
    filter_: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["filter"] = filter_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/v1/sites/{site_id}/hotspot/vouchers".format(
            site_id=site_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[VoucherDeletionResults]:
    if response.status_code == 200:
        response_200 = VoucherDeletionResults.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[VoucherDeletionResults]:
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
    filter_: str,
) -> Response[VoucherDeletionResults]:
    """Delete Vouchers

     Remove Hotspot vouchers based on the specified filter criteria.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`createdAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn` `like`|
    |`code`|`STRING`|`eq` `ne` `in` `notIn`|
    |`authorizedGuestLimit`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`authorizedGuestCount`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`activatedAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expiresAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expired`|`BOOLEAN`|`eq` `ne`|
    |`timeLimitMinutes`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`dataUsageLimitMBytes`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`rxRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`txRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    </details>

    Args:
        site_id (UUID):
        filter_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VoucherDeletionResults]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: str,
) -> Optional[VoucherDeletionResults]:
    """Delete Vouchers

     Remove Hotspot vouchers based on the specified filter criteria.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`createdAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn` `like`|
    |`code`|`STRING`|`eq` `ne` `in` `notIn`|
    |`authorizedGuestLimit`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`authorizedGuestCount`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`activatedAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expiresAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expired`|`BOOLEAN`|`eq` `ne`|
    |`timeLimitMinutes`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`dataUsageLimitMBytes`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`rxRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`txRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    </details>

    Args:
        site_id (UUID):
        filter_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VoucherDeletionResults
    """

    return sync_detailed(
        site_id=site_id,
        client=client,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: str,
) -> Response[VoucherDeletionResults]:
    """Delete Vouchers

     Remove Hotspot vouchers based on the specified filter criteria.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`createdAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn` `like`|
    |`code`|`STRING`|`eq` `ne` `in` `notIn`|
    |`authorizedGuestLimit`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`authorizedGuestCount`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`activatedAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expiresAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expired`|`BOOLEAN`|`eq` `ne`|
    |`timeLimitMinutes`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`dataUsageLimitMBytes`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`rxRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`txRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    </details>

    Args:
        site_id (UUID):
        filter_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VoucherDeletionResults]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    filter_: str,
) -> Optional[VoucherDeletionResults]:
    """Delete Vouchers

     Remove Hotspot vouchers based on the specified filter criteria.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`createdAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn` `like`|
    |`code`|`STRING`|`eq` `ne` `in` `notIn`|
    |`authorizedGuestLimit`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`authorizedGuestCount`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`activatedAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expiresAt`|`TIMESTAMP`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`expired`|`BOOLEAN`|`eq` `ne`|
    |`timeLimitMinutes`|`NUMBER`|`eq` `ne` `gt` `ge` `lt` `le`|
    |`dataUsageLimitMBytes`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`rxRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`txRateLimitKbps`|`NUMBER`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    </details>

    Args:
        site_id (UUID):
        filter_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VoucherDeletionResults
    """

    return (
        await asyncio_detailed(
            site_id=site_id,
            client=client,
            filter_=filter_,
        )
    ).parsed
