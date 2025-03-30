
from .base import Validator
from uuid import UUID


__all__ = [
    "UserCreateScheme",
    "UserScheme",
    "UserChangeIsAdmin",
    "UserDeleteScheme"
]


class UserCreateScheme(Validator):
    uuid: UUID | None
    yandex_id: str
    is_admin: bool
    login: str
    client_id: str
    real_name: str | None
    first_name: str
    last_name: str | None
    sex: str | None
    emails: list[str] | None
    birthday: str | None
    default_phone: str | None
    code: str
    cid: str


class UserScheme(UserCreateScheme):
    id: int


class UserChangeIsAdmin(Validator):
    id: int
    is_admin: bool


class UserDeleteScheme(Validator):
    id: int