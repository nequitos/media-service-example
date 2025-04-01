
from src.depends import uow


async def main():
    await uow.metadata_drop()
    await uow.metadata_create()


if __name__ == "__main__":
    import asyncio
    # from asyncio import get_event_loop
    #
    # loop = get_event_loop()
    # loop.run_until_complete(main())
    # asyncio.set_event_loop(loop)
    asyncio.run(main())