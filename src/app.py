
from fastapi import FastAPI
from uvicorn import Server, Config
from fastapi.middleware.cors import CORSMiddleware

from depends import uow
from src.routers import *


app = FastAPI()
app.include_router(auth_router)
app.include_router(media_router)
app.include_router(token_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"
    ],
)


async def main(host: str, port: int) -> None:
    config = Config(app="app:app", host=host, port=port, log_level="debug")
    server = Server(config=config)

    await uow.metadata_drop()
    await uow.metadata_create()
    await server.serve()


if __name__ == "__main__":
    import asyncio
    from config import HOST, PORT

    asyncio.run(main(HOST, PORT))