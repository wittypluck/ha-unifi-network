from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.latest_statistics_for_a_device import LatestStatisticsForADevice
from typing import cast
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    device_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/sites/{site_id}/devices/{device_id}/statistics/latest".format(site_id=site_id,device_id=device_id,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[LatestStatisticsForADevice]:
    if response.status_code == 200:
        response_200 = LatestStatisticsForADevice.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[LatestStatisticsForADevice]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_id: UUID,
    device_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[LatestStatisticsForADevice]:
    """ Get Latest Device Statistics

     Retrieve the latest real-time statistics of a specific adopted device, such as uptime, data
    transmission rates, CPU and memory utilization.

    Args:
        site_id (UUID):
        device_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LatestStatisticsForADevice]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
device_id=device_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_id: UUID,
    device_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[LatestStatisticsForADevice]:
    """ Get Latest Device Statistics

     Retrieve the latest real-time statistics of a specific adopted device, such as uptime, data
    transmission rates, CPU and memory utilization.

    Args:
        site_id (UUID):
        device_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LatestStatisticsForADevice
     """


    return sync_detailed(
        site_id=site_id,
device_id=device_id,
client=client,

    ).parsed

async def asyncio_detailed(
    site_id: UUID,
    device_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[LatestStatisticsForADevice]:
    """ Get Latest Device Statistics

     Retrieve the latest real-time statistics of a specific adopted device, such as uptime, data
    transmission rates, CPU and memory utilization.

    Args:
        site_id (UUID):
        device_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LatestStatisticsForADevice]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
device_id=device_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_id: UUID,
    device_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[LatestStatisticsForADevice]:
    """ Get Latest Device Statistics

     Retrieve the latest real-time statistics of a specific adopted device, such as uptime, data
    transmission rates, CPU and memory utilization.

    Args:
        site_id (UUID):
        device_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LatestStatisticsForADevice
     """


    return (await asyncio_detailed(
        site_id=site_id,
device_id=device_id,
client=client,

    )).parsed
