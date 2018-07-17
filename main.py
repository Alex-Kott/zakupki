import asyncio
import json

from aiohttp import ClientSession

index_url = "http://zakupki.mos.ru/#/offerauction"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with ClientSession() as session:
        async with session.get(index_url) as response:
            await response.text()

            api_request = "http://zakupki.mos.ru/api/Cssp/OfferAuction/PostQuery"
            payload = {"filter": {"stateIdIn": ["19000002"]},
                       "take": "5000",
                       "skip": 0,
                       "order": [{"field": "id",
                                  "desc": True}],
                       "withCount": True}

            response = await session.post(api_request, data=payload)
            raw_response = await response.text()
            print(raw_response)
            with open('response.json', 'w') as file:
                file.write(raw_response)


if __name__ == "__main__":
    asyncio.run(main())
