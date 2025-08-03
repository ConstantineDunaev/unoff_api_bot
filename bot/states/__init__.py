from aiogram.fsm.state import State, StatesGroup


class InputState(StatesGroup):
    default = State()
    input_name_market = State()
    input_curl_market = State()
