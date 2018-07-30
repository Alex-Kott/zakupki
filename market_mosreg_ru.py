import asyncio

from aiohttp import ClientSession


async def main():
    get_trades_url = "https://api.market.mosreg.ru/api/Trade/GetTradesForParticipantOrAnonymous"
    payload = {"page": 1,
               "itemsPerPage": 100,
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
            print(raw_response)
            # for k, v in response.__dict__.items():
            #     print(k)
            #     print(v, end='\n\n')

            with open('mosreg_response.json', 'w') as file:
                file.write(raw_response)


if __name__ == "__main__":
    asyncio.run(main())
