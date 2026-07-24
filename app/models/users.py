from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
)

from app.engine import metadata_obj

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), nullable=False, unique=True),
    Column("hashed_password", String(255), nullable=False),
)