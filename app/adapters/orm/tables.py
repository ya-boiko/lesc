"""Table definitions."""

from datetime import datetime, UTC

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    ForeignKey,
    String,
    DateTime
)
from sqlalchemy.dialects import postgresql


metadata = MetaData()

UUID = String().with_variant(postgresql.UUID(as_uuid=True), 'postgresql')
now_time = lambda: datetime.now(UTC)


accounts_table = Table(
    'accounts',
    metadata,
    Column('username', String, primary_key=True),
    Column('hashed_password', String, nullable=False),
)

# roles_table = Table(
#     'roles',
#     metadata,
#     Column('id', UUID, primary_key=True),
#     Column('name', String, nullable=False, unique=True)
# )
#
# participants_table = Table(
#     'participants',
#     metadata,
#     Column('id', UUID, primary_key=True),
#     Column('role_id', UUID, ForeignKey('roles.id'), primary_key=True, nullable=False, index=True),
#     Column('telegram_nickname', String, nullable=False, unique=True),
#     Column('created_at', DateTime, nullable=False, default=now_time),
#     Column('updated_at', DateTime, nullable=False, default=now_time, onupdate=now_time),
# )
