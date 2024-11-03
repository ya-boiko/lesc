"""Models."""

from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import Request


class AccessToken(BaseModel):
    """Successful login access token."""

    access_token: str
    token_type: str = "bearer"


@dataclass
class Credentials:
    """User login credentials."""

    username: str
    password: str

    @classmethod
    async def parse(cls, request: Request) -> "Credentials | None":
        """
        Parses request for credentials looking either into body as JSON
        or form data fields as required by OAuth2 spec.
        """

        data = {}

        if request.headers["content-type"] == "application/json":
            data = await request.json()

        elif request.headers["content-type"] == "application/x-www-form-urlencoded":
            data = await request.form()

        return Credentials(str(data["username"]), str(data["password"])) if data else None
