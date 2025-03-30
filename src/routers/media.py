
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

from src.utils.security.jwt import get_current_user, oauth2_scheme, validate_access_token
from src.schemes.user import UserScheme



audio_formats = [
    "aiff", "au", "mid", "midi", "mp3", "m4a", "mp4", "wav", "wma"
]
router = APIRouter(prefix="/media")


@router.post(
    "/upload"
)
async def upload(
    file: UploadFile,
    title: Annotated[str, None, Form()],
    user_scheme: Annotated[UserScheme, Depends(get_current_user)],
) -> Response:
    file_format = "".join(file.filename.split(".")[-1])
    if title is not None:
        filename = f"{title}.{file_format}"
    else:
        filename = file.filename


    file_location = f"resources/media/{user_scheme.id}/{filename}"
    user_dir_path = f"resources/media/{user_scheme.id}/"

    if not exists(user_dir_path):
        mkdir(user_dir_path)

    if file_format in audio_formats:
        with open(file_location, "wb+") as fl:
            fl.write(await file.read())

    return Response(
        content="Successful"
    )

