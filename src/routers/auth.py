
from httpx import AsyncClient
from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from src.depends import get_user_repository
from src.utils.security.jwt import create_access_token

from src.config import (
    YANDEX_AUTH_URL,
    YANDEX_TOKEN_URL,
    YANDEX_USER_INFO_URL,
    CLIENT_SECRET,
    CLIENT_ID,
    AUTH_REDIRECT_URI,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.schemes.user import UserCreateScheme, UserScheme
from src.schemes.token import TokenScheme, TokenDataScheme
from src.repositories.user import UserRepository


router = APIRouter(prefix="/auth")


@router.get(
    "/login"
)
async def login():
    return {
        "auth_url": f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={AUTH_REDIRECT_URI}"
    }


@router.get(
    "/callback",
    response_model=TokenScheme
)
async def callback(
    code: str | None = None,
    cid: str | None = None,
    repository: UserRepository = Depends(get_user_repository)
) -> TokenScheme:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    async with AsyncClient() as client:
        response = await client.post(YANDEX_TOKEN_URL, data=data)
        token_data = response.json()

        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Auth error")

        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = await client.get(YANDEX_USER_INFO_URL, headers=headers)
        user_info = user_response.json()

    is_admin = True if CLIENT_ID == user_info["client_id"] else False
    user_create_scheme = UserCreateScheme(
        yandex_id=user_info["id"],
        is_admin=is_admin,
        login=user_info["login"],
        client_id=user_info["client_id"],
        real_name=user_info["real_name"],
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        sex=user_info["sex"],
        emails=user_info["emails"],
        birthday=user_info["birthday"],
        default_phone=user_info["default_phone"],
        code=code,
        cid=cid
    )

    endpoint_scheme = await repository.create(scheme=user_create_scheme)
    if endpoint_scheme is not None:
        access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_info["first_name"]},
            expire_delta=access_token_expire
        )

        return TokenScheme(
            access_token=access_token,
            token_type="bearer"
        )
