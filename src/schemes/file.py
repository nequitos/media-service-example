
from .base import Validator


class FilesUploadScheme(Validator):
    filenames: list[str] | None