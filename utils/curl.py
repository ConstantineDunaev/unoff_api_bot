from json import dumps


def parse_cookies(raw_cookies: str):
    cookies = {}
    for item in raw_cookies.split(';'):
        pair = item.split('=')
        first_part = pair[0] if pair[0] else None
        second_part = pair[1] if len(pair) == 2 else None
        cookies[first_part.strip()] = second_part.strip()
    return cookies


def parse_curl(raw_curl: str) -> tuple:
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

    return dumps(headers), dumps(cookies)
