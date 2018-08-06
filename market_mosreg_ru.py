import asyncio
import json
from typing import Dict

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def parse_procurement(session: ClientSession, item: Dict[str, str]):
    headers = {
        "XXX-TenantId-Header": "2"
    }
    async with session.get(f"https://api.market.mosreg.ru/api/Trade/{item['Id']}/GetTradeDocuments", headers=headers) as response:
        raw_response = await response.text()
        data = json.loads(raw_response)
        file_links = [item["Url"] for item in data]

    async with session.get(f"https://market.mosreg.ru/Trade/ViewTrade", params={'id': item['Id']}) as response:
        raw_response = await  response.text()
        soup = BeautifulSoup(raw_response, "lxml")
        




async def main():
    get_trades_url = "https://api.market.mosreg.ru/api/Trade/GetTradesForParticipantOrAnonymous"
    payload = {"page": 1,
               "itemsPerPage": 1,
               "tradeState": "15",
               "OnlyTradesWithMyApplications": False,
               "sortingParams": [],
               "filterPriceMin": "",
               "filterPriceMax": "",
               "filterDateFrom": None,
               "filterDateTo": None,
               "filterFillingApplicationEndDateFrom": None,
               "FilterFillingApplicationEndDateTo": None,
               "filterTradeEasuzNumber": "",
               "showOnlyOwnTrades": False,
               "IsImmediate": False,
               "UsedClassificatorType": 10,
               "classificatorCodes": [], "CustomerFullNameOrInn": "", "CustomerAddress": "",
               "ParticipantHasApplicationsOnTrade": ""
               }
    headers = {
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        # "Connection": "keep-alive",
        # "Content-Type": "application/json; charset=UTF-8",
        # "DNT": "1",
        # "Host": "api.market.mosreg.ru",
        # "Origin": "https://market.mosreg.ru",
        # "Referer": "https://market.mosreg.ru/",
        # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "XXX-TenantId-Header": "2"
    }
    async with ClientSession() as session:
        async with session.post(get_trades_url, headers=headers, data=payload) as response:
            raw_response = await response.text()
            # print(raw_response)
            # for k, v in response.__dict__.items():
            #     print(k)
            #     print(v, end='\n\n')

            # with open('mosreg_response.json', 'w') as file:
            #     file.write(raw_response)

            data = json.loads(raw_response)

            procurement_list = data['invdata']

            procurements = [await parse_procurement(session, item) for item in procurement_list]










if __name__ == "__main__":
    asyncio.run(main())
