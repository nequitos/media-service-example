
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2AuthorizationCodeBearer
)

from src.config import (
    SECRET_KEY,
    ALGORITHM
)

from src.schemes.token import TokenDataScheme
from src.schemes.user import UserScheme
from src.repositories.user import UserRepository
from src.depends import get_user_repository


__all__ = [
    "oauth2_scheme",
    "create_access_token",
    "validate_access_token",
    "get_current_user"
]



oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/docs",
    tokenUrl="bearer"
)


def create_access_token(
    data: dict,
    expire_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def validate_access_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenDataScheme | None:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    if username:
        return TokenDataScheme(username=username)


async def get_current_user(
    token: Annotated[str, oauth2_scheme],
    repository: UserRepository
) -> UserScheme:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        token_data_scheme = validate_access_token(token)
        if token_data_scheme is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user_scheme = await repository.read(
        username=token_data_scheme.username
    )

    if user_scheme is None:
        raise credentials_exception
    else:
        return user_scheme