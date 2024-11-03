"""Endpoints."""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette.status import HTTP_204_NO_CONTENT

from app.domain import commands
from app.service_layer.message_bus import MessageBus

from .models import AccessToken, Credentials
from .middleware import get_current_account


router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/login")
@inject
async def login(
    request: Request,
    response: Response,
    bus: MessageBus = Depends(Provide["bus"]),
    jwt_expiration_delta_hours: int = Depends(Provide["config.auth.jwt_expiration_delta_hours"]),
) -> AccessToken:
    """Logs the user in and returns either the token (sets the cookie) or 401 Unauthorized."""
    credentials = await Credentials.parse(request)

    cmd = commands.Authenticate(username=credentials.username, passwd=credentials.password)
    account = bus.handle(cmd).pop()

    if not account:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    cmd = commands.GenerateToken(username=credentials.username)
    token = bus.handle(cmd).pop()

    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=3600 * jwt_expiration_delta_hours,
    )

    return AccessToken(access_token=token)


@router.delete(
    "/logout",
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_account)],
    response_model=None,
)
def logout(response: Response) -> None:
    """Logs the user out."""
    response.set_cookie(
        key="Authorization",
        value="",
        httponly=True,
        max_age=-1,
    )
