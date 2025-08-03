from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from bot.filters import IsAdmin
from resources import Buttons, Texts
from bot.keyboards.inline import get_scripts_keyboard
from db import Connection
from bot.callback_factory import ScriptChoice
from scripts import captions, functions
from utils.script import run_script


scripts_router = Router()
scripts_router.message.filter(IsAdmin())


@scripts_router.message(F.text == Buttons.scripts)
async def scripts_handler(message: Message):
    await message.answer(Texts.scripts,
                         reply_markup=get_scripts_keyboard())


@scripts_router.callback_query(ScriptChoice.filter())
async def run_script_handler(callback_query: CallbackQuery,
                             callback_data: ScriptChoice,
                             connection: Connection,
                             bot: Bot):
    script = callback_data.script

    func = functions[script]
    caption = captions[script]
    await callback_query.message.edit_text(text=Texts.script_runned.format(caption=caption),
                                           reply_markup=None)

    await run_script(connection=connection,
                     bot=bot,
                     func=func,
                     caption=caption,
                     users={callback_query.from_user.id})



