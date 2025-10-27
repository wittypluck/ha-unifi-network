from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_overview_page import ClientOverviewPage
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    *,
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params["filter"] = filter_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/clients".format(site_id=site_id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientOverviewPage]:
    if response.status_code == 200:
        response_200 = ClientOverviewPage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientOverviewPage]:
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
    filter_: Union[Unset, str] = UNSET,

) -> Response[ClientOverviewPage]:
    """ List Connected Clients

     Retrieve a paginated list of all connected clients on a site, including physical devices (computers,
    smartphones) and active VPN connections.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`macAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`ipAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`connectedAt`|`TIMESTAMP`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`access.type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`access.authorized`|`BOOLEAN`|`isNull` `isNotNull` `eq` `ne`|
    </details>

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientOverviewPage]
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
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[ClientOverviewPage]:
    """ List Connected Clients

     Retrieve a paginated list of all connected clients on a site, including physical devices (computers,
    smartphones) and active VPN connections.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`macAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`ipAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`connectedAt`|`TIMESTAMP`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`access.type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`access.authorized`|`BOOLEAN`|`isNull` `isNotNull` `eq` `ne`|
    </details>

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientOverviewPage
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
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Response[ClientOverviewPage]:
    """ List Connected Clients

     Retrieve a paginated list of all connected clients on a site, including physical devices (computers,
    smartphones) and active VPN connections.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`macAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`ipAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`connectedAt`|`TIMESTAMP`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`access.type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`access.authorized`|`BOOLEAN`|`isNull` `isNotNull` `eq` `ne`|
    </details>

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientOverviewPage]
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
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[ClientOverviewPage]:
    """ List Connected Clients

     Retrieve a paginated list of all connected clients on a site, including physical devices (computers,
    smartphones) and active VPN connections.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`macAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`ipAddress`|`STRING`|`isNull` `isNotNull` `eq` `ne` `in` `notIn`|
    |`connectedAt`|`TIMESTAMP`|`isNull` `isNotNull` `eq` `ne` `gt` `ge` `lt` `le`|
    |`access.type`|`STRING`|`eq` `ne` `in` `notIn`|
    |`access.authorized`|`BOOLEAN`|`isNull` `isNotNull` `eq` `ne`|
    </details>

    Args:
        site_id (UUID):
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientOverviewPage
     """


    return (await asyncio_detailed(
        site_id=site_id,
client=client,
offset=offset,
limit=limit,
filter_=filter_,

    )).parsed
