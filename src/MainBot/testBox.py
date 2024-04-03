import threading
import time
import asyncio

lock = threading.Lock()

shared_list = []
def addMsg(item):
    shared_list.append(item)

def notifyMsgs(loop):
    with lock:
        # print(shared_list)
        time.sleep(1)
        for i in shared_list:
            if not i.is_empty():
                future = asyncio.run_coroutine_threadsafe(i.send(), loop)
                future.result()
    

def while_loop(loop):
    while True:
        notifyMsgs(loop)
        time.sleep(5)


