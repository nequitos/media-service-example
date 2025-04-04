import os

from environs import Env
from os.path import exists
from os import mkdir


if not exists("resources"):
    os.mkdir("resources")
if not exists("resources/media"):
    os.mkdir("resources/media")


env = Env()
env.read_env()

POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT")
POSTGRES_DATABASE = env.str("POSTGRES_DATABASE")

YANDEX_AUTH_URL = env.str("YANDEX_AUTH_URL")
YANDEX_TOKEN_URL = env.str("YANDEX_TOKEN_URL")
YANDEX_USER_INFO_URL = env.str("YANDEX_USER_INFO_URL")
AUTH_REDIRECT_URI = env.str("AUTH_REDIRECT_URI")

CLIENT_ID = env.str("CLIENT_ID")
CLIENT_SECRET = env.str("CLIENT_SECRET")

USERNAME = env.str("USERNAME")
PASSWORD = env.str("PASSWORD")

SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
HOST = env.str("HOST")
PORT = env.int("PORT")