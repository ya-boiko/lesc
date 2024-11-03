"""ORM."""

from sqlalchemy.orm import registry
from app.adapters.orm import instrumentation

from app.adapters.orm import tables
from app.domain import models


mapper_registry = registry()
metadata = tables.metadata

instrumentation.instrument_entity()


def bind_mappers():
    """Binds ORM mappers"""

    mapper_registry.map_imperatively(models.Account, tables.accounts_table)
