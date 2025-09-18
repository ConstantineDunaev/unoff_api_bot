from aiohttp import ClientSession
from json import dumps
from typing import List
from schemas.supply_wb import SupplyDetailWB
from resources import Texts


async def get_supply_details_wb(headers: dict, cookies: dict, supply_id: int) -> List[SupplyDetailWB]:
    result = []
    data = {
        "params":
            {
                "pageNumber": 1,
                "pageSize": 100,
                "preorderID": None,
                "search": "",
                "supplyID": supply_id
            },
        "jsonrpc": "2.0",
        "id": "json-rpc_85"
    }
    url = "https://seller-supply.wildberries.ru/ns/sm-supply/supply-manager/api/v1/supply/supplyDetails"
    async with ClientSession(headers=headers,
                             cookies=cookies) as session:
        response = await session.post(url=url,
                                      data=dumps(data))
        if response.status == 401:
            raise RuntimeError(Texts.error_401)

        data = await response.json()
        for item in data['result']['data']:
            barcode = item.get('barcode')
            sa = item.get('sa')
            quantity = item.get('quantity')
            unloading_quantity = item.get('unloadingQuantity')
            ready_for_sale_quantity = item.get('readyForSaleQuantity')
            income_quantity = item.get('incomeQuantity')
            nm_id = item.get('nmID')
            if barcode:
                result.append(
                    SupplyDetailWB(
                        barcode=barcode,
                        sa=sa,
                        quantity=quantity,
                        unloading_quantity=unloading_quantity,
                        ready_for_sale_quantity=ready_for_sale_quantity,
                        income_quantity=income_quantity,
                        nm_id=nm_id
                    )
                )
    return result
