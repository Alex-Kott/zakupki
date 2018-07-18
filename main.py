import asyncio
import json

from aiohttp import ClientSession

index_url = "http://zakupki.mos.ru/#/offerauction"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def foo():
    """
    filter:
        stateIdIn:
            19000002 - активная
            19000003 - не состоялась
            19000004 - проведена
            19000005 - снята с публикации


    :return:
    """

async def parse_entities(session, entities):
    for entity in entities:
        response = await session.get("http://zakupki.mos.ru/api/Cssp/OfferAuction/GetEntity")
        entity_data = await response.text()
        with open("entity.json", "w") as file:
            file.write(entity_data)


async def main():
    async with ClientSession() as session:
        async with session.get(index_url) as response:
            await response.text()  # делаем запрос для получения кук

            api_request = "http://zakupki.mos.ru/api/Cssp/OfferAuction/PostQuery"
            payload = {"filter": {"stateIdIn": ["19000002"]},
                       # "take": "10",
                       "skip": 0,
                       "order": [{"field": "id",
                                  "desc": True}],
                       "withCount": True}

            # response = await session.post(api_request, data=payload)
            # raw_response = await response.text()
            # print(raw_response)
            # with open('response.json', 'w') as file:
            #     file.write(raw_response)

            with open('response.json') as file:
                data = json.loads(file.read())

            """получаем активные котировки"""
            entites = [item for item in data['items'] if item['state']['name'] == "Активная"]
            for entity in entites:
                await parse_entities(session, entity)








if __name__ == "__main__":
    asyncio.run(main())
