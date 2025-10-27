from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.site_overview_page import SiteOverviewPage
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
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
        "url": "/v1/sites",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SiteOverviewPage]:
    if response.status_code == 200:
        response_200 = SiteOverviewPage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SiteOverviewPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Response[SiteOverviewPage]:
    """ List Local Sites

     Retrieve a paginated list of local sites managed by this Network application.
    Site ID is required for other UniFi Network API calls.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`internalReference`|`STRING`|`eq` `ne` `in` `notIn`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn`|
    </details>

    Args:
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SiteOverviewPage]
     """


    kwargs = _get_kwargs(
        offset=offset,
limit=limit,
filter_=filter_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[SiteOverviewPage]:
    """ List Local Sites

     Retrieve a paginated list of local sites managed by this Network application.
    Site ID is required for other UniFi Network API calls.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`internalReference`|`STRING`|`eq` `ne` `in` `notIn`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn`|
    </details>

    Args:
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SiteOverviewPage
     """


    return sync_detailed(
        client=client,
offset=offset,
limit=limit,
filter_=filter_,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Response[SiteOverviewPage]:
    """ List Local Sites

     Retrieve a paginated list of local sites managed by this Network application.
    Site ID is required for other UniFi Network API calls.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`internalReference`|`STRING`|`eq` `ne` `in` `notIn`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn`|
    </details>

    Args:
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SiteOverviewPage]
     """


    kwargs = _get_kwargs(
        offset=offset,
limit=limit,
filter_=filter_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    offset: Union[Unset, Any] = 0,
    limit: Union[Unset, Any] = 25,
    filter_: Union[Unset, str] = UNSET,

) -> Optional[SiteOverviewPage]:
    """ List Local Sites

     Retrieve a paginated list of local sites managed by this Network application.
    Site ID is required for other UniFi Network API calls.

    <details>
    <summary>Filterable properties (click to expand)</summary>

    |Name|Type|Allowed functions|
    |-|-|-|
    |`id`|`UUID`|`eq` `ne` `in` `notIn`|
    |`internalReference`|`STRING`|`eq` `ne` `in` `notIn`|
    |`name`|`STRING`|`eq` `ne` `in` `notIn`|
    </details>

    Args:
        offset (Union[Unset, Any]):  Default: 0.
        limit (Union[Unset, Any]):  Default: 25.
        filter_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SiteOverviewPage
     """


    return (await asyncio_detailed(
        client=client,
offset=offset,
limit=limit,
filter_=filter_,

    )).parsed
