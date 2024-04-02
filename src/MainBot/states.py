from aiogram.fsm.state import StatesGroup, State


class Promts(StatesGroup):
    reg_prompt = State()
    add_con_prompt = State()
    add_reg_prompt = State()
    del_prompt = State()
