
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import URL

from src.repositories import *
from src.config import *


# --- Database initialize --- #
postgres_url = URL.create(
    "postgresql+asyncpg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DATABASE
)
engine = create_async_engine(url=postgres_url)
uow = UoW(engine=engine)


# --- Repositories initialize --- #
uow[User] = UserRepository


def get_user_repository() -> UserRepository:
    return uow[User]
