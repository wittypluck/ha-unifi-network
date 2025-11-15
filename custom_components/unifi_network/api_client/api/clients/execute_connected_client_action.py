from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_action_request import ClientActionRequest
from ...models.client_action_response import ClientActionResponse
from uuid import UUID


def _get_kwargs(
    site_id: UUID,
    client_id: UUID,
    *,
    body: ClientActionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sites/{site_id}/clients/{client_id}/actions".format(
            site_id=site_id,
            client_id=client_id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ClientActionResponse]:
    if response.status_code == 200:
        response_200 = ClientActionResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ClientActionResponse]:
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
    body: ClientActionRequest,
) -> Response[ClientActionResponse]:
    """Execute Client Action

     Perform an action on a specific connected client. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        client_id (UUID):
        body (ClientActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientActionResponse]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        client_id=client_id,
        body=body,
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
    body: ClientActionRequest,
) -> Optional[ClientActionResponse]:
    """Execute Client Action

     Perform an action on a specific connected client. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        client_id (UUID):
        body (ClientActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientActionResponse
    """

    return sync_detailed(
        site_id=site_id,
        client_id=client_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ClientActionRequest,
) -> Response[ClientActionResponse]:
    """Execute Client Action

     Perform an action on a specific connected client. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        client_id (UUID):
        body (ClientActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientActionResponse]
    """

    kwargs = _get_kwargs(
        site_id=site_id,
        client_id=client_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    site_id: UUID,
    client_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ClientActionRequest,
) -> Optional[ClientActionResponse]:
    """Execute Client Action

     Perform an action on a specific connected client. The request body must include the action name and
    any applicable input arguments.

    Args:
        site_id (UUID):
        client_id (UUID):
        body (ClientActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientActionResponse
    """

    return (
        await asyncio_detailed(
            site_id=site_id,
            client_id=client_id,
            client=client,
            body=body,
        )
    ).parsed
