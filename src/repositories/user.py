
from sqlalchemy import (
    insert,
    update,
    delete,
    select
)
from .base import Repository, User

from src.schemes.user import *


class UserRepository(Repository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create(self, scheme: UserCreateScheme) -> UserCreateScheme:
        stmt = insert(User).values(
            yandex_id=scheme.id,
            login=scheme.login,
            client_id=scheme.client_id,
            real_name=scheme.real_name,
            first_name=scheme.first_name,
            last_name=scheme.last_name,
            sex=scheme.sex,
            emails=scheme.emails,
            birthday=scheme.birthday,
            default_phone=scheme.default_phone,
            code=scheme.code,
            cid=scheme.cid
        )

        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

        return scheme

    async def get_by_name(self, username: str) -> UserScheme | None:
        stmt = select(User).where(first_name=username)

        async with self._session() as session:
            result = await session.execute(stmt)

        return result.scalar_one_or_none()


