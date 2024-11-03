"""Account model."""

from dataclasses import dataclass
from typing import Optional

import bcrypt

from .entity import Entity


@dataclass
class Account(Entity):
    """User account."""

    username: str
    hashed_password: Optional[str] = None

    def __post_init__(self):
        super().__init__()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Account) and self.username == o.username

    def __hash__(self) -> int:
        return hash(self.username)

    @classmethod
    def hashpw(cls, passwd):
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(passwd.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def checkpw(self, passwd):
        """Checks if a password matches the hashed password."""
        return bcrypt.checkpw(passwd.encode("utf8"), self.hashed_password.encode("utf8"))

