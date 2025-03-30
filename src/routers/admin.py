
from typing import Annotated
from passlib.context import CryptContext

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from src.utils.security.jwt import (
    get_current_user
)
from src.repositories.user import UserRepository
from src.depends import get_user_repository
from src.schemes.user import (
    UserScheme,
    UserChangeIsAdmin,
    UserDeleteScheme
)

router = APIRouter(prefix="/admin", tags=["Administration"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_denied_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access denied"
)


@router.get(
    "/get_user",
    response_model=UserScheme
)
async def get_user(
    _id: int,
    user_scheme: Annotated[UserScheme, Depends(get_current_user)],
    repository: UserRepository = Depends(get_user_repository),
) -> UserScheme | HTTPException | None:
    if user_scheme.is_admin:
        endpoint_scheme = await repository.read(_id=_id)

        return endpoint_scheme
    else:
        return access_denied_error


@router.delete(
    "/delete_user",
    response_model=UserDeleteScheme
)
async def delete_user(
    _id: int,
    user_scheme: Annotated[UserScheme, Depends(get_current_user)],
    repository: UserRepository = Depends(get_user_repository)
) -> bool | HTTPException:
    if user_scheme.is_admin:
        endpoint_result = await repository.delete(_id=_id)

        return endpoint_result
    else:
        return access_denied_error


@router.put(
    "/change_is_admin",
    response_model=UserScheme
)
async def change_is_admin(
    scheme: UserChangeIsAdmin,
    user_scheme: Annotated[UserScheme, Depends(get_current_user)],
    repository: UserRepository = Depends(get_user_repository)
) -> UserScheme | HTTPException:
    if user_scheme.is_admin:
        endpoint_scheme = await repository.update(scheme)

        return endpoint_scheme
    else:
        return access_denied_error

