"""Account repository."""

from app.adapters.repo import SqlAlchemyRepository

from app.service_layer.repositories import AccountRepository
from app.domain import models


class SqlAlchemyAccountRepository(SqlAlchemyRepository, AccountRepository):
    """Sqlalchemy account repository."""

    model_type = models.Account
