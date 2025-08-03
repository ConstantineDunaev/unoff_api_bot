from db import connection_context
from scripts import functions, captions
from enums import Scripts
from config import Config
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from sys import argv
from asyncio import run
from utils.script import run_script


async def main():
    if len(argv) == 1:
        return

    script = argv[1]
    if script not in (item for item in Scripts):
        return

    caption = captions[script]
    func = functions[script]

    default = DefaultBotProperties(parse_mode='HTML',
                                   link_preview_is_disabled=True)
    async with Bot(token=Config.TELEGRAM_TOKEN, default=default) as bot:
        async with connection_context() as connection:
            await run_script(connection=connection,
                             bot=bot,
                             func=func,
                             caption=caption,
                             users=Config.TELEGRAM_USERS)


if __name__ == '__main__':
    run(main())
