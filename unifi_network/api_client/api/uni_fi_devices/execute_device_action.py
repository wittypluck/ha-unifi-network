from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.device_action_request import DeviceActionRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    device_id: UUID,
    *,
    body: DeviceActionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sites/{site_id}/devices/{device_id}/actions".format(site_id=site_id,device_id=device_id,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    body: DeviceActionRequest,

) -> Response[Any]:
    """ Execute Device Action

     Perform an action on an specific adopted device. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        device_id (UUID):
        body (DeviceActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
device_id=device_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    site_id: UUID,
    device_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: DeviceActionRequest,

) -> Response[Any]:
    """ Execute Device Action

     Perform an action on an specific adopted device. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        device_id (UUID):
        body (DeviceActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
device_id=device_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

