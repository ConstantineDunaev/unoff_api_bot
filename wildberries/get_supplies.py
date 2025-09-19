from aiohttp import ClientSession
from json import dumps
from typing import List
from schemas.supply_wb import SupplyWB
from resources import Texts


async def get_supplies_wb(headers: dict, cookies: dict) -> List[SupplyWB]:
    result = []
    data = {
        "params":
            {
                "pageNumber": 1,
                "pageSize": 100,
                "sortBy": "createDate",
                "sortDirection": "desc",
                "statusId": -2,
                "searchById": None
            },
        "jsonrpc": "2.0",
        "id": "json-rpc_34"
    }
    url = "https://seller-supply.wildberries.ru/ns/sm-supply/supply-manager/api/v1/supply/listSupplies"
    async with ClientSession(headers=headers,
                             cookies=cookies) as session:

        response = await session.post(url=url,
                                      data=dumps(data))
        if response.status == 401:
            raise RuntimeError(Texts.error_401)

        data = await response.json()

        for item in data['result']['data']:
            supply_id = item.get('supplyId')
            supply_date = item.get('supplyDate')
            fact_date = item.get('factDate')
            if supply_id and supply_date:
                result.append(
                    SupplyWB(
                        supply_id=supply_id,
                        supply_date=supply_date,
                        fact_date=fact_date
                    )
                )
    return result
