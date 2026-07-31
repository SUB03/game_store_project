import uuid
from sqlalchemy import (
    Table,
    Column,
    Integer,
    Text,
    UUID,
    DateTime
)

from auth_service.engine import metadata_obj

users_table = Table(
    "auth_users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", Text, nullable=False, unique=True),
    Column("hashed_password", Text, nullable=False),
    Column("email", Text, nullable=False, unique=True)
)

token_whitelist = Table(
    "auth_token_whitelist",
    metadata_obj,
    Column("uid", UUID, primary_key=True, default=uuid.uuid4), #jti of the refresh token
    Column("expiration_at", DateTime(timezone=True), nullable=False),
)