import logging
import asyncio
import time
import Heap

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from MainBot import config
from MainBot import handler
import threading
from MainBot.testBox import *

ioloop = asyncio.get_event_loop()

heap = Heap()

async def main():
    bot = Bot(config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handler.router)
    thread1 = threading.Thread(target=while_loop, args=(ioloop,))
    thread1.daemon = True
    thread1.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ioloop.run_until_complete(ioloop.create_task(main()))
    ioloop.close()
