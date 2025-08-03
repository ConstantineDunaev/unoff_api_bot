from aiohttp import ClientSession
from json import dumps
from typing import List
from schemas.discount_wb import DiscountWB


async def get_discount_wb(headers: dict, cookies: dict) -> List[DiscountWB]:
    result = []
    limit = 1000
    offset = 0
    data = {
        "limit": limit,
        "offset": 0,
        "facets": [],
        "filterWithoutPrice": False,
        "filterWithLeftovers": False,
        "sort": "price",
        "sortOrder": 0
    }
    url = "https://discounts-prices.wildberries.ru/ns/dp-api/discounts-prices/suppliers/api/v1/list/goods/filter"
    async with ClientSession(headers=headers,
                             cookies=cookies) as session:
        while True:
            data["offset"] = offset
            response = await session.post(url=url,
                                          data=dumps(data))
            data = await response.json()
            goods = data['data']['listGoods']
            for good in goods:
                result.append(
                    DiscountWB(nm_id=good.get('nmID'),
                               vendor_code=good.get('vendorCode'),
                               discount_on_site=good.get('discountOnSite'))
                )
            if len(goods) < limit:
                break
            offset += len(goods)
    return result
