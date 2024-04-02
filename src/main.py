import asyncio

import MainBot
import Heap
import threading

mainBot = None
heap = None

def main():

    mainBot = MainBot.MainBot()
    heap = Heap.Heap()

    mainBotThread = threading.Thread(target=mainBot.run)
    heapThread = threading.Thread(target=heap.run)

    mainBotThread.start()
    heapThread.start()

    mainBotThread.join()
    heapThread.join()


# if __name__ == "__main__":
#     main()


import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from MainBot import config
from MainBot import handler


async def main():
    bot = Bot(config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
