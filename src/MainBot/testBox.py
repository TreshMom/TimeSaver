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
    

def while_loop(self):
    while True:
        now = datetime.now()
        minMessage = self.heap[0]
        minMessageTime = minMessage.time
        if now - minMessageTime > timedelta(minutes=5):
            if not self.heap[0].is_empty():
                future = asyncio.run_coroutine_threadsafe(self.heap[0].send(), loop)
                future.result()
                break
        time.sleep(5)


