from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hotspot_voucher_creation_request import HotspotVoucherCreationRequest
from ...models.integration_voucher_creation_result_dto import IntegrationVoucherCreationResultDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    site_id: UUID,
    *,
    body: HotspotVoucherCreationRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/sites/{site_id}/hotspot/vouchers".format(site_id=site_id,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[IntegrationVoucherCreationResultDto]:
    if response.status_code == 201:
        response_201 = IntegrationVoucherCreationResultDto.from_dict(response.json())



        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[IntegrationVoucherCreationResultDto]:
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
    body: HotspotVoucherCreationRequest,

) -> Response[IntegrationVoucherCreationResultDto]:
    """ Generate Vouchers

     Create one or more Hotspot vouchers.

    Args:
        site_id (UUID):
        body (HotspotVoucherCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationVoucherCreationResultDto]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotspotVoucherCreationRequest,

) -> Optional[IntegrationVoucherCreationResultDto]:
    """ Generate Vouchers

     Create one or more Hotspot vouchers.

    Args:
        site_id (UUID):
        body (HotspotVoucherCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationVoucherCreationResultDto
     """


    return sync_detailed(
        site_id=site_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotspotVoucherCreationRequest,

) -> Response[IntegrationVoucherCreationResultDto]:
    """ Generate Vouchers

     Create one or more Hotspot vouchers.

    Args:
        site_id (UUID):
        body (HotspotVoucherCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationVoucherCreationResultDto]
     """


    kwargs = _get_kwargs(
        site_id=site_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: HotspotVoucherCreationRequest,

) -> Optional[IntegrationVoucherCreationResultDto]:
    """ Generate Vouchers

     Create one or more Hotspot vouchers.

    Args:
        site_id (UUID):
        body (HotspotVoucherCreationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationVoucherCreationResultDto
     """


    return (await asyncio_detailed(
        site_id=site_id,
client=client,
body=body,

    )).parsed
