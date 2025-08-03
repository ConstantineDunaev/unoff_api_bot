from aiogram.fsm.state import State, StatesGroup


class InputState(StatesGroup):
    default = State()
    create_market_input_name = State()
    create_market_input_curl = State()
    update_market_input_curl = State()
