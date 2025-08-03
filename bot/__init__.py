from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from mysql import MySQLPool
from .handlers import routers
from .middlewares import UpdateMiddleware


async def create_bot(token: str) -> Bot:
    default = DefaultBotProperties(parse_mode='HTML',
                                   link_preview_is_disabled=True)
    bot = Bot(token=token,
              default=default)
    await bot.delete_webhook()
    return bot


async def start_bot(bot: Bot):
    dp = Dispatcher()
    dp.include_routers(*routers)
    dp.update.outer_middleware(UpdateMiddleware())
    allowed_updates = ["message", "callback_query"]
    await dp.start_polling(bot, allowed_updates=allowed_updates)

