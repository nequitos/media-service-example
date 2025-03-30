
from .base import Validator


class TokenScheme(Validator):
    access_token: str
    token_type: str = "bearer"


class TokenDataScheme(Validator):
    uuid: str | None = None


class TokenAuthorizeScheme(Validator):
    access_token: str
