"""Middleware."""

from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED

from app.domain import models, commands
from app.service_layer.message_bus import MessageBus


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """Adds support for access token passed via cookie."""

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization") or request.cookies.get("Authorization")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")


def decode_token(
    token: str,
    bus: MessageBus = Provide["bus"],
) -> models.Account | None:
    """Attempts to decode the token and return the account."""
    cmd = commands.DecodeToken(token=token)
    accounts = bus.handle(cmd)

    if not accounts:
        return None

    return accounts.pop()


@inject
def get_current_account(
    access_token: str = Depends(oauth2_scheme),
) -> models.Account:
    """Uses access token to get authenticated user account.

    Raises 401 if access token is invalid or missing.
    """
    account = decode_token(token=access_token)

    if not account:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return account
