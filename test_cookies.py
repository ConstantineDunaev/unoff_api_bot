from json import loads, dumps
from aiohttp import ClientSession


def parse_cookies(raw_cookies: str):
    cookies = {}
    for item in raw_cookies.split(';'):
        pair = item.split('=')
        first_part = pair[0] if pair[0] else None
        second_part = pair[1] if len(pair) == 2 else None
        cookies[first_part.strip()] = second_part.strip()
    return cookies


def parse_curl(raw_curl: str):
    cookies = dict()
    headers = dict()

    raw_curl = [item.strip() for i, item in enumerate(raw_curl.split('\\')) if i]

    for item in raw_curl:
        pair = item.replace('-H ', '').replace('-b ', '').strip("'").split(': ')
        first_part = pair[0] if pair[0] else None
        second_part = pair[1] if len(pair) == 2 else None

        if first_part and second_part:
            headers[first_part] = second_part
        elif first_part and not second_part:
            if not first_part.startswith('--data-raw'):
                cookies = parse_cookies(first_part)

    return headers, cookies


async def main():
    with open('curl.txt', encoding='utf-8') as f:
        curl = f.read()
    data = {"limit": 1000,
            "offset": 0,
            "facets": [],
            "filterWithoutPrice": False,
            "filterWithLeftovers": False,
            "sort": "price",
            "sortOrder": 0}
    headers, cookies = parse_curl(curl)
    url = "https://discounts-prices.wildberries.ru/ns/dp-api/discounts-prices/suppliers/api/v1/list/goods/filter"
    result = []
    async with ClientSession(headers=headers,
                             cookies=cookies) as session:
        while True:
            data["limit"] = 1000
            data["offset"] = len(result)
            response = await session.post(url=url,
                                          data=dumps(data))
            data = await response.json()
            goods = data['data']['listGoods']
            if not goods:
                break
            result += goods
    return result


if __name__ == '__main__':
    from asyncio import run

    print(run(main()))
