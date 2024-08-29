from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse

from comms_api.authentication.authentication import JWTBearer
from comms_api.core.events import create_stateful_events, send_stateless_events
from comms_api.models.events import StatefulEvents, StatelessEvents
from comms_api.routers.exceptions import HTTPError
from comms_api.routers.utils import timeout
from wazuh.core.exception import WazuhEngineError, WazuhError


@timeout(30)
async def post_stateful_events(events: StatefulEvents) -> JSONResponse:
    """Post stateful events handler.

    Parameters
    ----------
    events : StatefulEvents
        Stateful events list.

    Raises
    ------
    HTTPError
        If there is any error when indexing the events.

    Returns
    -------
    JSONResponse
        Indexer response.
    """
    try:
        response = await create_stateful_events(events)
        return JSONResponse(response)
    except WazuhError as exc:
        raise HTTPError(message=exc.message, status_code=status.HTTP_400_BAD_REQUEST)


@timeout(10)
async def post_stateless_events(events: StatelessEvents) -> Response:
    """Post stateless events handler.

    Parameters
    ----------
    events : StatelessEvents
        Stateless events list.

    Raises
    ------
    HTTPError
        If there is any error when communicating with the engine.

    Returns
    -------
    Response
        HTTP OK empty response.
    """
    try:
        await send_stateless_events(events)
        return Response(status_code=status.HTTP_200_OK)
    except WazuhEngineError as exc:
        raise HTTPError(message=exc.message, code=exc.code, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


events_router = APIRouter(prefix='/events')
events_router.add_api_route('/stateful', post_stateful_events, dependencies=[Depends(JWTBearer())], methods=['POST'])
events_router.add_api_route('/stateless', post_stateless_events, dependencies=[Depends(JWTBearer())], methods=['POST'])
