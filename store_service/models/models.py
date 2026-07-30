from sqlalchemy import (
    Table,
    Column,
    Integer,
    Numeric,
    BigInteger,
    DateTime,
    Identity,
    Text,
    Boolean,
    ForeignKey
)

from store_service.engine import metadata_obj

games = Table(
    "games",
    metadata_obj,
    Column("appid", BigInteger, Identity(), primary_key=True),
    Column("name", Text, nullable=False),
    Column("release_date", DateTime, nullable=False),
    Column("required_age", Integer, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column("discount", Integer, nullable=False),
    Column("dlc_count", Integer, nullable=False),
    Column("detailed_description", Text),
    Column("about_the_game", Text),
    Column("short_description", Text),
    Column("reviews", Text),
    Column("header_image", Text),
    Column("website", Text),
    Column("support_url", Text),
    Column("support_email", Text),
    Column("windows", Boolean),
    Column("mac", Boolean),
    Column("linux", Boolean),
    Column("metacritic_score", Integer),
    Column("metacritic_url", Text),
    Column("achievements", Integer, nullable=False),
    Column("recommendations", Integer),
    Column("notes", Text),
    Column("positive", Integer),
    Column("negative", Integer),
)

developers = Table(
    "developers",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("developers", Text, primary_key=True)
)

publishers = Table(
    "publishers",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("publishers", Text, primary_key=True)
)

game_text_languages = Table(
    "game_text_languages",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("language", Text, primary_key=True),
)

game_audio_languages = Table(
    "game_audio_languages",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("language", Text, primary_key=True),
)

categories = Table(
    "categories",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("categories", Text, primary_key=True)
)
genres = Table(
    "genres",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("genres", Text, primary_key=True)
)
tags = Table(
    "tags",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("tags", Text, primary_key=True)
)
screenshots = Table(
    "screenshots",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("screenshots", Text, primary_key=True)
)

movies = Table(
    "movies",
    metadata_obj,
    Column("appid", BigInteger, ForeignKey("games.appid"), primary_key=True),
    Column("movies", Text, primary_key=True)
)