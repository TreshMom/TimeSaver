from typing import Union

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
from .testBox import *

from .states import States

from TgClient import TgClient

from . import kb, text, utils

router = Router()


@router.message(Command("start"))
@router.message(F.text == "Начать работу")
async def start_handler(msg: Message):
    await msg.answer(text.greet1.format(name=msg.from_user.full_name), reply_markup=kb.exit_kb)
    await msg.answer(text.greet2.format(name=msg.from_user.full_name), reply_markup=kb.menu_greet)


@router.message(Command("menu"))
@router.message(F.text == "Меню")
async def menu(msg: Message, state: FSMContext):
    await state.set_state(States.main_menu)
    await msg.answer(text.menu, reply_markup=kb.menu_main)


@router.callback_query(F.data == "registration")
async def input_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.reg_prompt)
    await clbck.message.answer(text.reg_text)


@router.message(States.reg_prompt)
async def registration(msg: Message, state: FSMContext):
    api_id, api_hash = map(lambda st: st.strip(), msg.text.split(","))
    mesg = await msg.answer(f"api_id :{api_id}, api_hash : {api_hash}")
    res = await utils.registration(state, api_id, api_hash)
    if res == -1:
        await mesg.edit_text(text.error_text)
    elif res == 1:
        await msg.answer(text.aut_text)
        await state.set_state(States.aut_prompt)


@router.message(States.aut_prompt)
async def get_phone_and_password(msg: Message, state: FSMContext):
    phone, password = map(lambda st: st.strip(), msg.text.split(","))
    mesg = await msg.answer(f"{phone}, {password}")
    res = await utils.auntification(state, phone, password)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        # res = await utils
        print("get_phone")
        # await msg.answer(text.telephone_text)
        # await state.set_state(States.phone_prompt)



async def get_auntification(msg: Message):
    phone, password = map(lambda st: st.strip(), msg.text.split(","))
    return phone, password


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

