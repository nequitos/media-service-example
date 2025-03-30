
from typing import Annotated
from os.path import exists
from os import mkdir

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Request,
    Response,
    Depends,
    Form
)
from fastapi.responses import RedirectResponse

from src.utils.security.jwt import oauth2_scheme, get_current_user
from src.schemes.file import FilesUploadScheme
from src.schemes.token import TokenScheme
from src.repositories.user import UserRepository
from src.depends import get_user_repository


audio_formats = [
    "aiff", "au", "mid", "midi", "mp3", "m4a", "mp4", "wav", "wma"
]
router = APIRouter(prefix="/media")


@router.post(
    "/upload"
)
async def upload(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    file: UploadFile,
    title: Annotated[str, None, Form()] = None,
    repository: UserRepository = Depends(get_user_repository),

):
    print(access_token)
    file_format = "".join(file.filename.split(".")[-1])
    if title is not None:
        filename = f"{title}.{file_format}"
    else:
        filename = file.filename

    user_scheme = await get_current_user(access_token, repository)

    file_location = f"resources/media/{user_scheme.id}/{filename}"
    user_dir_path = f"resources/media/{user_scheme.id}/"

    if not exists(user_dir_path):
        mkdir(user_dir_path)

    if file_format in audio_formats:
        with open(file_location, "wb+") as fl:
            fl.write(await file.read())

