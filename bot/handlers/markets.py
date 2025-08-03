from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.filters import IsAdmin, StateFilter
from resources import Buttons, Texts
from bot.keyboards.reply import get_markets_keyboard, get_back_keyboard
from bot.keyboards.inline import get_market_control_keyboard
from bot.states import InputState
from db import Connection
from services.market import get_markets, create_market, update_market, get_market
from bot.callback_factory import MarketControl
from enums import MarketAction
from utils.curl import parse_curl
from datetime import datetime
from schemas.market import NewMarket, UpdateMarket, GetMarket

markets_router = Router()
markets_router.message.filter(IsAdmin())


@markets_router.message(F.text == Buttons.markets)
@markets_router.message(F.text == Buttons.back,
                        StateFilter(InputState.create_market_input_name,
                                    InputState.create_market_input_curl,
                                    InputState.update_market_input_curl))
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
            reply_markup = get_market_control_keyboard(market)
            await message.answer(text,
                                 reply_markup=reply_markup)


@markets_router.message(F.text == Buttons.add_market)
async def input_name_market_handler(message: Message, state: FSMContext):
    """Ввод имени для Маркета"""
    await state.set_state(InputState.create_market_input_name)
    await message.answer(text=Texts.input_name_market,
                         reply_markup=get_back_keyboard())


@markets_router.message(InputState.create_market_input_name)
async def input_curl_market_handler(message: Message, state: FSMContext):
    """Ввод curl для Маркета"""
    await state.set_data({"market_name": message.text})
    await state.set_state(InputState.create_market_input_curl)
    await message.answer(text=Texts.input_curl_market,
                         reply_markup=get_back_keyboard())


@markets_router.message(InputState.create_market_input_curl)
async def create_market_handler(message: Message, state: FSMContext, connection: Connection):
    """Создание Маркета"""
    data = await state.get_data()
    name = data.get('market_name')
    curl = message.text

    await state.set_data({})
    await state.set_state(InputState.default)

    headers, cookies = parse_curl(curl)
    new_market = NewMarket(name=name,
                           headers=headers,
                           cookies=cookies,
                           is_active=True,
                           updated_at=datetime.now())

    market = await create_market(connection=connection,
                                 new_market=new_market)

    text = Texts.added_market.format(name=name)
    await message.answer(text,
                         reply_markup=get_markets_keyboard())

    text = Texts.market_view.format(market_id=market.market_id,
                                    name=market.name,
                                    updated_at=market.updated_at.strftime("%d.%m.%Y %H:%M:%S"))
    reply_markup = get_market_control_keyboard(market)
    await message.answer(text,
                         reply_markup=reply_markup)


@markets_router.callback_query(MarketControl.filter(F.action == MarketAction.update))
async def update_cookies_handler(callback_query: CallbackQuery, state: FSMContext, callback_data: MarketControl):
    """Обработка нажатия кнопки Обновить cookies"""
    await callback_query.answer()
    market_id = callback_data.market_id
    await state.set_data({"market_id": market_id})
    await state.set_state(InputState.update_market_input_curl)
    await callback_query.message.answer(text=Texts.input_curl_market,
                                        reply_markup=get_back_keyboard())


@markets_router.message(InputState.update_market_input_curl)
async def update_market_handler(message: Message, state: FSMContext, connection: Connection):
    """Обновление Маркета"""
    curl = message.text

    data = await state.get_data()
    market_id = data.get('market_id')
    await state.set_data({})
    await state.set_state(InputState.default)

    market = await get_market(connection, GetMarket(market_id=market_id))

    headers, cookies = parse_curl(curl)
    upd_market = UpdateMarket(market_id=market.market_id,
                              name=market.name,
                              headers=headers,
                              cookies=cookies,
                              is_active=market.is_active,
                              updated_at=market.updated_at)

    market = await update_market(connection=connection,
                                 upd_market=upd_market)

    text = Texts.updated_market.format(name=market.name)
    await message.answer(text,
                         reply_markup=get_markets_keyboard())

    text = Texts.market_view.format(market_id=market.market_id,
                                    name=market.name,
                                    updated_at=market.updated_at.strftime("%d.%m.%Y %H:%M:%S"))
    reply_markup = get_market_control_keyboard(market)
    await message.answer(text,
                         reply_markup=reply_markup)
