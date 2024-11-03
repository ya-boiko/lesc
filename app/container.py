"""Container."""

from dependency_injector import containers, providers
from sqlalchemy import create_engine, orm

from app.adapters.unit_of_work import UnitOfWork
from app.service_layer.handlers import mapping
from app.service_layer.message_bus import MessageBus


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""

    wiring_config = containers.WiringConfiguration(
        packages=['app'],
    )

    config = providers.Configuration()

    database_engine = providers.Singleton(
        create_engine,
        config.database.url,
        echo=True,
        pool_recycle=3600,
        pool_pre_ping=True,
    )

    session_factory = providers.Factory(
        orm.sessionmaker,
        autocommit=False,
        autoflush=False,
        bind=database_engine,
        expire_on_commit=False,
    )

    uow = providers.Factory(UnitOfWork, session_factory)

    # Bus

    event_handlers = providers.Object(mapping.EVENT_HANDLERS)
    command_handlers = providers.Object(mapping.COMMAND_HANDLERS)
    bus = providers.Singleton(MessageBus, uow, event_handlers, command_handlers)
