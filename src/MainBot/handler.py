from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
from .testBox import *

from .states import States

from . import kb, text, utils

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state : FSMContext):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_greet)


@router.message(Command("menu"))
@router.message(F.text == "◀️ Выйти в меню")
# @router.message(States.main_menu)
async def menu(msg: Message, state: FSMContext):
    await state.set_state(States.main_menu)
    await msg.answer(text.menu, reply_markup=kb.menu_main)


@router.callback_query(F.data == "registration")
async def input_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.reg_prompt)
    await clbck.message.answer(text.reg_text)
    # await menu(msg, state)


@router.message(States.reg_prompt)
async def registration(msg: Message, state: FSMContext):
    api_id, api_hash = map(lambda st: st.strip(), msg.text.split(","))
    mesg = await msg.answer(f"api_id :{api_id}, api_hash : {api_hash}")
    res = await utils.registration(state, api_id, api_hash)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text(text.reg_text_correct)


@router.callback_query(F.data == "add_contact")
async def input_add_con_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.add_con_prompt)
    await clbck.message.answer(text.add_con_text, reply_markup=kb.exit_kb)


@router.message(States.add_con_prompt)
async def add_contact(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.add_contact(state, prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text(text.add_con_text_correct)
        await menu(msg, state)


@router.callback_query(F.data == "delete_contact")
async def input_del_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.del_prompt)
    await clbck.message.answer(text.del_text, reply_markup=kb.exit_kb)


@router.message(States.del_prompt)
async def add_regular_massage(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.delete_contact(state, prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text(text.add_reg_text_correct)
        await menu(msg, state)


@router.callback_query(F.data == "add_regular_massage")
async def input_add_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.add_reg_prompt)
    await clbck.message.answer(text.add_reg_text, reply_markup=kb.exit_kb)


@router.message(States.add_reg_prompt)
async def add_regular_massage(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.add_regular_massage(state, prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text(text.add_reg_text_correct)
        await menu(msg, state)


