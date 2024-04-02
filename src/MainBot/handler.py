from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext

# from ..TgClient import TgClient

from .states import States

from . import kb, text, utils

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_greet)


@router.message(Command("menu"))
@router.message(F.text == "◀️ Выйти в меню")
@router.message(States.main_menu)
async def menu(msg: Message, state: FSMContext):
    await state.set_state(States.main_menu)
    await msg.answer(text.menu, reply_markup=kb.menu_main)


@router.callback_query(F.data == "registration")
async def input_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.reg_prompt)
    await clbck.message.answer(text.reg_text)


# @router.message(F.text)
# async def answerMsg(msg: Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state == Promts.reg_prompt:
#         api_id, api_hash = map(lambda st: st.strip(), msg.text.split(","))
#         await state.set_data({"client": TgClient(api_id, api_hash)})
#         await msg.answer(f"api_id :{api_id}, api_hash : {api_hash}")
#     if current_state == Promts.add_con_prompt:
#         name = msg.text
#         state.get_data()["client"].subscribe_user(name)


@router.message(States.reg_prompt)
async def registration(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.registration(prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text("красава")
        await state.set_state(States.main_menu)


@router.callback_query(F.data == "add_contact")
async def input_add_con_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.add_con_prompt)
    await clbck.message.edit_text(text.add_con_text)
    await clbck.message.answer(text.reg_text, reply_markup=kb.exit_kb)


@router.message(States.add_con_prompt)
async def add_contact(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.add_contact(prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text("красава")
        await state.set_state(States.main_menu)


@router.callback_query(F.data == "delete_contact")
async def input_del_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.del_prompt)
    await clbck.message.edit_text(text.del_text)
    await clbck.message.answer(text.del_text, reply_markup=kb.exit_kb)


@router.message(States.del_prompt)
async def add_regular_massage(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.delete_contact(prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text("красава")
        await state.set_state(States.main_menu)


@router.callback_query(F.data == "add_regular_massage")
async def input_add_reg_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.add_reg_prompt)
    await clbck.message.edit_text(text.add_reg_text)
    await clbck.message.answer(text.add_reg_text, reply_markup=kb.exit_kb)


@router.message(States.add_reg_prompt)
async def add_regular_massage(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.check_text)
    res = await utils.add_regular_massage(prompt)
    if res == -1:
        await mesg.edit_text(text.error_text)
    else:
        await mesg.edit_text("красава")
        await state.set_state(States.main_menu)
