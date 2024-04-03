from typing import Any, Dict, Optional
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from TgClient import TgClient
from . import testBox
from datetime import *
import aiogram.types
from . import text

async def registration(context: FSMContext, api_id: str, api_hash: str):
    try:
        client = TgClient(api_id, api_hash)
        await context.set_data({"client": client})
        res = await client.run()
        if res == 1:
            return 1
        return 2
    except Exception as e:
        print(e)
        return -1


async def set_phone_password(context: FSMContext, phone: str, password: str):
    client = (await context.get_data())['client']
    client.set_phone_password(phone, password)


async def get_code(context: FSMContext):
    client = (await context.get_data())['client']
    await client.send_code_request()


async def run_bot(msg: aiogram.types.Message, context: FSMContext, code: str):
    client = (await context.get_data())['client']
    client.set_code(code)
    try:
        await client.run()
        await msg.answer(text.reg_text_correct)
    except Exception as e:
        print(e)
        return -1


async def add_contact(context: FSMContext, info: str):
    try:
        (await context.get_data())["client"].subscribe_user(info)
        return 1
    except Exception as e:
        print("add_content")
        print(e)
        return -1


async def delete_contact(context: FSMContext, info: str):
    try:
        (await context.get_data())["client"].unsubscribeUser(info)
        return 1
    except Exception as e:
        print(e)
        return -1


async def add_regular_massage(context: FSMContext, to: str, text_to_reply: str, begin : datetime, period: timedelta):
    print(to, text_to_reply, begin, period)
    client = (await context.get_data())["client"]
    testBox.addMsg(Message.MessageSchedule(period, begin, client, to, text_to_reply))
    return 1
