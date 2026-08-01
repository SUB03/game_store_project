from sqlalchemy import (
    Table,
    Column,
    MetaData,
    Integer,
    BigInteger,
    ForeignKey,
    Identity,
)

metadata = MetaData()

# reference
games = Table(
    "store_games",
    metadata,
    Column("appid", BigInteger, Identity(), primary_key=True),
    extend_existing=True
)

users_table = Table(
    "auth_users",
    metadata,
    Column("id", Integer, primary_key=True),
    extend_existing=True
)

games_ownership = Table(
    "users_game_ownership",
    metadata,
    Column("id", Integer, ForeignKey("auth_users.id"), primary_key=True),
    Column("appid", BigInteger, ForeignKey("store_games.appid"), primary_key=True),
)