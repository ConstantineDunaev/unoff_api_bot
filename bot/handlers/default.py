from aiogram import Router, F
from aiogram.types import Message
from bot.filters import IsAdmin
from bot.keyboards.reply import get_main_keyboard

default_router = Router()


@default_router.message(F.text, IsAdmin())
async def handler_default_admin(message: Message):
    await message.answer("Меню:",
                         reply_markup=get_main_keyboard())


@default_router.message(F.text)
async def handler_start_user(message: Message):
    await message.answer("У вас нет доступа к фукнционалу бота.")
