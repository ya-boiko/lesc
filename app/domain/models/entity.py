"""Entity model."""

from app.domain.events import Event


class Entity:
    """Entity with events."""

    events: list[Event]

    def __init__(self) -> None:
        self.events = []
