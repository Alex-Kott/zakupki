import asyncio
import csv
import json
from collections import OrderedDict
from typing import Dict

from aiohttp import ClientSession


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def filter_fields(entity) -> Dict[str, str]:
    files = []
    file_download_url = "http://zakupki.mos.ru/api/Core/FileStorage/GetDownload"
    for file in entity['files']:
        files.append(f"{file_download_url}/?fileHash={file['fileStorage']['fileHash']}")

    row = OrderedDict([
        ('customer', entity['company']['name']),
        ('endDate', entity['endDate']),
        ('companyCustomerRegionName', entity['companyCustomerRegionName']),
        ('name', entity['name']),
        ('startCost', entity['startCost']),
        ('maxDays', entity['maxDays']),
        ('fileLinks', '\n'.join(files))
    ])

    return row


def get_header() -> OrderedDict:
    header = OrderedDict([
        ('customer', "Заказчик"),
        ('endDate', "Дата окончания"),
        ('companyCustomerRegionName', "Регион"),
        ('name', "Название"),
        ('startCost', "Начальная стоиомость"),
        ('maxDays', "Дней на поставку"),
        ('fileLinks', "Ссылки на файлы"),
    ])

    return header


def save_entities_data(data):
    header = get_header()
    with open("data.csv", "w") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([v for k, v in header.items()])

    with open("data.csv", "a") as file:
        dict_writer = csv.DictWriter(file, header, delimiter=';')
        dict_writer.writerows(data)


async def parse_entities(session, entity):
    get_entity_url = "http://zakupki.mos.ru/api/Cssp/OfferAuction/GetEntity"
    response = await session.get(get_entity_url, params={'id': entity['id']})
    raw_data = await response.text()
    entity_data = json.loads(raw_data)
    with open("entity.json", "w") as file:
        file.write(raw_data)

    return filter_fields(entity_data)


async def get_all_entities(session):
    """
    Запрос почему-то возвращает абсолютно все котировки за всё время независимо от параметров,
    но вообще возможные значения фильтра такие:
    filter:
        stateIdIn:
            19000002 - активная
            19000003 - не состоялась
            19000004 - проведена
            19000005 - снята с публикации
    """
    api_request = "http://zakupki.mos.ru/api/Cssp/OfferAuction/PostQuery"
    payload = {"filter": {"stateIdIn": []},
               # "take": "10",
               "skip": 0,
               "order": [{"field": "id",
                          "desc": True}],
               "withCount": True}

    response = await session.post(api_request, data=payload)

    return await response.text()


async def main():
    async with ClientSession() as session:
        index_url = "http://zakupki.mos.ru/#/offerauction"
        async with session.get(index_url) as response:
            await response.text()  # делаем запрос для получения кук

            # raw_response = await get_all_entities(session)
            # data = json.load(raw_response)
            # with open('response.json', 'w') as file:
            #     file.write(raw_response)
            with open('response.json') as file:
                data = json.loads(file.read())

            """получаем активные котировки"""
            entites = [item for item in data['items'] if item['state']['name'] == "Активная"]
            total_entities = len(entites)

            entities_info = []
            for counter, entity in enumerate(entites):
                print(f"{counter+1}/{total_entities}", end='\r', flush=True, sep='')
                entities_info.append(await parse_entities(session, entity))

                save_entities_data(entities_info)

            print('')


if __name__ == "__main__":
    asyncio.run(main())
