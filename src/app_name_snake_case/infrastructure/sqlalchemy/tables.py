from sqlalchemy import (
    Column,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    Uuid,
)


metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Uuid(), primary_key=True, nullable=False),
    Column("name", String(), nullable=False, unique=True),
    UniqueConstraint("name", name="users_name_unique"),
)
