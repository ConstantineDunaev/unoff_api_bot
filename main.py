from asyncio import run
from config import Config
from bot import create_bot, start_bot
import logging


async def main():
    bot = await create_bot(token=Config.TELEGRAM_TOKEN)
    await start_bot(bot=bot)


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(name)s: %(message)s",
                        level=logging.DEBUG)
    run(main())
