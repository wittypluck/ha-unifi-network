from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hotspot_voucher_detail_page import HotspotVoucherDetailPage
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    *,
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 100,
    filter_: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params["filter"] = filter_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/hotspot/vouchers".format(site_id=site_id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[HotspotVoucherDetailPage]:
    if response.status_code == 200:
        response_200 = HotspotVoucherDetailPage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[HotspotVoucherDetailPage]:
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
    limit: Union[Unset, Any] = 100,
    filter_: Union[Unset, str] = UNSET,

) -> Response[HotspotVoucherDetailPage]:
    """ List Vouchers

     Retrieve a paginated list of Hotspot vouchers.

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
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 100.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotspotVoucherDetailPage]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
offset=offset,
limit=limit,
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
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 100,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[HotspotVoucherDetailPage]:
    """ List Vouchers

     Retrieve a paginated list of Hotspot vouchers.

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
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 100.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotspotVoucherDetailPage
     """


    return sync_detailed(
        site_id=site_id,
client=client,
offset=offset,
limit=limit,
filter_=filter_,

    ).parsed

async def asyncio_detailed(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 100,
    filter_: Union[Unset, str] = UNSET,

) -> Response[HotspotVoucherDetailPage]:
    """ List Vouchers

     Retrieve a paginated list of Hotspot vouchers.

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
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 100.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HotspotVoucherDetailPage]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
offset=offset,
limit=limit,
filter_=filter_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 100,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[HotspotVoucherDetailPage]:
    """ List Vouchers

     Retrieve a paginated list of Hotspot vouchers.

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
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 100.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HotspotVoucherDetailPage
     """


    return (await asyncio_detailed(
        site_id=site_id,
client=client,
offset=offset,
limit=limit,
filter_=filter_,

    )).parsed
