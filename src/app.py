
from fastapi import FastAPI
from uvicorn import Server, Config

from depends import uow
from src.routers import *


app = FastAPI()
app.include_router(auth_router)


async def main(host: str, port: int):
    config = Config(app="app:app", host=host, port=port, log_level="debug")
    server = Server(config=config)

    await uow.metadata_create()
    await server.serve()


if __name__ == "__main__":
    import asyncio
    from config import HOST, PORT

    asyncio.run(main(HOST, PORT))