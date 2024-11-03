"""Auth command handlers."""

from datetime import datetime, timedelta, UTC
from gettext import gettext as _

from dependency_injector.wiring import Provide, inject
import jwt

from app.domain import commands, models
from app.domain.errors import NotFound
from app.service_layer.unit_of_work import UnitOfWork


@inject
def generate_token(
    cmd: commands.GenerateToken,
    uow: UnitOfWork,
    jwt_secret: str = Provide["config.auth.jwt_secret"],
    jwt_expiration_delta_hours: int = Provide["config.auth.jwt_expiration_delta_hours"],
) -> str:
    """Takes claims and generates a JWT token."""
    with uow:
        account = _find_account_or_error(uow, cmd.username)

        iat = datetime.now(UTC)
        expires_in_seconds = jwt_expiration_delta_hours * 3600

        payload = {
            "username": account.username,
            "sub": account.username,
            "iat": iat,
            "nbf": iat,
            "exp": iat + timedelta(seconds=expires_in_seconds),
        }

        return jwt.encode(payload, jwt_secret, algorithm="HS256")


@inject
def decode_token(
    cmd: commands.DecodeToken,
    uow: UnitOfWork,
    jwt_secret: str = Provide["config.auth.jwt_secret"],
) -> models.Account | None:
    """Attempts to decode the token and return the account."""
    try:
        payload = jwt.decode(cmd.token, jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    else:
        with uow:
            return _find_account_or_error(uow, payload["username"])


def authentication(
    cmd: commands.Authenticate,
    uow: UnitOfWork,
) -> models.Account | None:
    """Authenticates the user.

    Returns the account if authentication was successful or None if it wasn't.
    """
    with uow:
        try:
            account = _find_account_or_error(uow, cmd.username)
        except NotFound:
            return None

        if not account.checkpw(cmd.passwd):
            return None

        return account


def _find_account_or_error(uow: UnitOfWork, username: str) -> None | models.Account:
    """Find an account by username or raise a NotFound exception."""
    account = uow.accounts.get(entity_id=username)

    if not account:
        raise NotFound(_("Account not found."))

    return account
