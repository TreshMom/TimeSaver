from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
from states import Promts

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
    # await clbck.message.answer(text., reply_markup=kb.exit_kb)


@router.message(Command("name"))
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu_main)
