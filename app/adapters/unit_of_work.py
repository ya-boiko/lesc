"""Unit of work."""

from app.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from app.service_layer.unit_of_work import UnitOfWork as IUnitOfWork
from app.service_layer.repositories import AccountRepository
from app.adapters.repo.account_repository import SqlAlchemyAccountRepository


class UnitOfWork(SqlAlchemyUnitOfWork, IUnitOfWork):
    """UoW."""

    accounts: AccountRepository = None

    def __init__(self, session_factory) -> None:
        super().__init__(session_factory)

    def _init_repositories(self, session) -> list[object]:
        self.accounts = SqlAlchemyAccountRepository(session)

        return [
            self.accounts,
        ]
