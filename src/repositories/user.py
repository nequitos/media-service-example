
from uuid import UUID

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
            uuid=scheme.uuid,
            is_admin=scheme.is_admin,
            yandex_id=scheme.yandex_id,
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

    async def read(
        self,
        _id: int | None = None,
        uuid: UUID | None = None
    ) -> UserScheme | None:
        if _id is not None:
            stmt = select(User).filter_by(id=_id)
        elif uuid is not None:
            stmt = select(User).filter_by(uuid=uuid)
        else:
            stmt = None

        if stmt is not None:
            async with self._session() as session:
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()

        if user.is_admin and user is not None:
            return UserScheme(
                id=user.id,
                uuid=user.uuid,
                yandex_id=user.yandex_id,
                is_admin=user.is_admin,
                login=user.login,
                client_id=user.client_id,
                real_name=user.real_name,
                first_name=user.first_name,
                last_name=user.last_name,
                sex=user.sex,
                emails=user.emails,
                birthday=user.birthday,
                default_phone=user.default_phone,
                code=user.code,
                cid=user.cid
            )

    async def delete(self, _id) -> bool:
        stmt = delete(User).where(User.id == _id)

        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

        return True

    async def update(self, scheme: UserChangeIsAdmin) -> UserScheme:
        stmt = update(User).where(User.id == scheme.id).values(
            is_admin=scheme.is_admin
        )

        async with self._session() as session:
            await session.execute(stmt)
            await session.commit()

        return await self.read(_id=scheme.id)



