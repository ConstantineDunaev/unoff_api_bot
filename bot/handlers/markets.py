from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.filters import IsAdmin, StateFilter
from bot.resources import Buttons, Texts
from bot.keyboards.reply import get_markets_keyboard, get_back_keyboard
from bot.states import InputState
from db import Connection
from services.market import get_markets, create_market

markets_router = Router()
markets_router.message.filter(IsAdmin())


@markets_router.message(F.text == Buttons.markets)
@markets_router.message(F.text == Buttons.back,
                        StateFilter(InputState.input_name_market, InputState.input_curl_market))
async def markets_handler(message: Message, state: FSMContext):
    """Раздел управления Маркетами"""
    await state.set_data({})
    await state.set_state(InputState.default)
    await message.answer(text=Texts.markets,
                         reply_markup=get_markets_keyboard())


@markets_router.message(F.text == Buttons.list_markets)
async def list_markets_handler(message: Message, connection: Connection):
    """Получение списка текущих Маркетов"""
    markets = await get_markets(connection)
    if markets:
        for market in markets:
            text = Texts.market_view.format(market_id=market.market_id,
                                            name=market.name,
                                            updated_at=market.updated_at.strftime("%d.%m.%Y %H:%M:%S"))
            await message.answer(text)


@markets_router.message(F.text == Buttons.add_market)
async def input_name_market_handler(message: Message, state: FSMContext):
    """Ввод имени для Маркета"""
    await state.set_state(InputState.input_name_market)
    await message.answer(text=Texts.input_name_market,
                         reply_markup=get_back_keyboard())


@markets_router.message(InputState.input_name_market)
async def input_curl_market_handler(message: Message, state: FSMContext):
    """Ввод curl для Маркета"""
    await state.set_data({"market_name": message.text})
    await state.set_state(InputState.input_curl_market)
    await message.answer(text=Texts.input_curl_market,
                         reply_markup=get_back_keyboard())


@markets_router.message(InputState.input_curl_market)
async def create_market_handler(message: Message, state: FSMContext, connection: Connection):
    """Создание Маркета"""
    data = await state.get_data()
    name = data.get('market_name')
    curl = message.text

    await state.set_data({})
    await state.set_state(InputState.default)

    market = await create_market(connection=connection,
                                 name=name,
                                 curl=curl)

    await message.answer(Texts.added_market,
                         reply_markup=get_markets_keyboard())

    text = Texts.market_view.format(market_id=market.market_id,
                                    name=market.name,
                                    updated_at=market.updated_at.strftime("%d.%m.%Y %H:%M:%S"))
    await message.answer(text)
