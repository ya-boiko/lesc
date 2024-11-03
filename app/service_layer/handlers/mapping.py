"""Events and commands mapping to handlers."""

from app.domain import events, commands
from app.service_layer import handlers

EVENT_HANDLERS = {}

COMMAND_HANDLERS = {
    commands.GenerateToken: handlers.generate_token,
    commands.DecodeToken: handlers.decode_token,
    commands.Authenticate: handlers.authentication,
}
