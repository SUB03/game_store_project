import uuid
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    UUID,
    DateTime
)

from app.engine import metadata_obj

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30), nullable=False, unique=True),
    Column("hashed_password", String(255), nullable=False),
)

token_whitelist = Table(
    "token_whitelist",
    metadata_obj,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4), #jti of the refresh token
    Column("expiration_at", DateTime(timezone=True), nullable=False),
)