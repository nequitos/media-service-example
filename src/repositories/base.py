
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any, Annotated
from pydantic._internal._model_construction import ModelMetaclass

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, BigInteger, ARRAY


T = TypeVar("T", bound=Any)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    yandex_id: Mapped[str] = mapped_column(String, nullable=False)
    login: Mapped[str] = mapped_column(String, nullable=False)
    client_id: Mapped[str] = mapped_column(String, nullable=False)
    real_name: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    sex: Mapped[str] = mapped_column(String, nullable=True)
    emails: Mapped[list[str]] = mapped_column(ARRAY(item_type=String), nullable=True)
    birthday: Mapped[str] = mapped_column(String, nullable=True)
    default_phone: Mapped[str] = mapped_column(String, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    cid: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"""
        User(
        id={self.id!r}
        )
        """


class Repository(Generic[T]):
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession] | None = None,
    ):
        super().__init__()
        self._session = session

        if session is None:
            raise Exception


class UoW(object):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__()
        self._engine = engine
        self._session = async_sessionmaker(bind=self._engine)

        self.__repositories = {}

    def __setitem__(
        self,
        entity_type: DeclarativeAttributeIntercept,
        repository: type
    ) -> None:
        self.__repositories[entity_type] = repository(self._session)

    def __getitem__(self, entity_type: DeclarativeAttributeIntercept) -> Repository[T]:
        return self.__repositories[entity_type]

    def __delitem__(self, entity_type: DeclarativeAttributeIntercept) -> None:
        del self.__repositories[entity_type]

    def __str__(self):
        return str(self.__repositories)

    async def metadata_create(self):
        async with self._engine.begin() as core:
            await core.run_sync(Base.metadata.create_all)

    async def metadata_drop(self):
        async with self._engine.begin() as core:
            await core.run_sync(Base.metadata.drop_all)
