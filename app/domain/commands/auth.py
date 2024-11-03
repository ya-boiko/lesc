"""Auth commands."""

from dataclasses import dataclass

from .command import Command


@dataclass
class GenerateToken(Command):
    username: str


@dataclass
class DecodeToken(Command):
    token: str


@dataclass
class Authenticate(Command):
    username: str
    passwd: str