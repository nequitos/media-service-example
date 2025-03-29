
from .base import Validator


class TokenScheme(Validator):
    access_token: str
    token_type: str


class TokenDataScheme(Validator):
    username: str | None = None
