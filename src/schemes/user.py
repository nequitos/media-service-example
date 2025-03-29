
from .base import Validator


class UserCreateScheme(Validator):
    id: str
    login: str
    client_id: str
    real_name: str
    first_name: str
    last_name: str
    sex: str
    emails: list[str]
    birthday: str
    default_phone: str | None
    code: str
    cid: str


class UserScheme(UserCreateScheme):
    id: int