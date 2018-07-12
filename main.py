import asyncio

from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        pass


if __name__ == "__main__":
    asyncio.run(main())