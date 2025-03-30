
from typing import Annotated

from fastapi import APIRouter, Depends, Form

from src.utils.security.jwt import validate_access_token
from src.schemes.token import TokenDataScheme


router = APIRouter(prefix="/bearer")


@router.post(
    ""
)
async def index(password: Annotated[str, Form()]) -> str:
    return password

