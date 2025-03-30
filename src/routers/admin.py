
from passlib.context import CryptContext

from fastapi import APIRouter

from src.utils.security.jwt import (
    create_access_token,
    validate_access_token,
    get_current_user
)

router = APIRouter(prefix="/admin")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

