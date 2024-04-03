from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    main_menu = State()
    reg_prompt = State()
    aut_prompt = State()
    add_con_prompt = State()
    add_reg_prompt = State()
    del_prompt = State()
