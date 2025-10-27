from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_details import ClientDetails
from typing import cast
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    client_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/clients/{client_id}".format(site_id=site_id,client_id=client_id,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientDetails]:
    if response.status_code == 200:
        response_200 = ClientDetails.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ClientDetails]:
    """ Get Connected Client Details

     Retrieve detailed information about a specific connected client, including name, IP address, MAC
    address, connection type and access information.

    Args:
        site_id (UUID):
        client_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientDetails]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
client_id=client_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ClientDetails]:
    """ Get Connected Client Details

     Retrieve detailed information about a specific connected client, including name, IP address, MAC
    address, connection type and access information.

    Args:
        site_id (UUID):
        client_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientDetails
     """


    return sync_detailed(
        site_id=site_id,
client_id=client_id,
client=client,

    ).parsed

async def asyncio_detailed(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ClientDetails]:
    """ Get Connected Client Details

     Retrieve detailed information about a specific connected client, including name, IP address, MAC
    address, connection type and access information.

    Args:
        site_id (UUID):
        client_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientDetails]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
client_id=client_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ClientDetails]:
    """ Get Connected Client Details

     Retrieve detailed information about a specific connected client, including name, IP address, MAC
    address, connection type and access information.

    Args:
        site_id (UUID):
        client_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientDetails
     """


    return (await asyncio_detailed(
        site_id=site_id,
client_id=client_id,
client=client,

    )).parsed
