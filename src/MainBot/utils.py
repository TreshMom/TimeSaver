from typing import Any, Dict, Optional
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from TgClient import TgClient
from . import testBox
import Message 
from datetime import *


async def registration(context: FSMContext, api_id: str, api_hash: str):
    try:
        client = TgClient(api_id, api_hash)
        await context.set_data({"client" : client})
        await client.run()
        await client.client.run_until_disconnected()
        return 1
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
        await context.get_data()["client"].unsubscribeUser(info)
        return 1
    except Exception as e:
        print(e)
        return -1


async def add_regular_massage(context: FSMContext, text_to_reply : str):
    client = (await context.get_data())["client"]
    for i in client.subscribed_users:
        testBox.addMsg(Message.MessageOnce(datetime.now() + timedelta(seconds=5),
                                        client, i, text_to_reply))
    return 1

# def help():
#     pass
