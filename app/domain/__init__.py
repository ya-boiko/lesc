"""Domain."""

from typing import Union

from app.domain import commands
from app.domain import events
from app.domain import models

Message = Union[commands.Command, events.Event]
