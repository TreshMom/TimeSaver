from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
from .states import Promts

from TgClient import TgClient

from . import kb, text, utils

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_greet)


@router.message(Command("menu"))
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_main)


@router.callback_query(F.data == "registration")
async def input_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Promts.reg_prompt)
    await clbck.message.answer(text.reg_text)


@router.message(Command("name"))
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_main)


@router.message(F.text)
async def answerMsg(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Promts.reg_prompt:
        api_id, api_hash = map(lambda st: st.strip(), msg.text.split(","))
        await state.set_data({"client" : TgClient(api_id,api_hash)})
        await msg.answer(f"api_id :{api_id}, api_hash : {api_hash}")
    if current_state == Promts.add_con_prompt:
        name = msg.text
        state.get_data()["client"].subscribe_user(name)
        

@router.callback_query(F.data == "add_contact")
async def addContact(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Promts.add_con_prompt)
    await clbck.message.answer(text.conn_text)