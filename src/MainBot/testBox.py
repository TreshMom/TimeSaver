import threading
import time
import asyncio
from datetime import datetime, timedelta
from Heap import Heap

lock = threading.Lock()
heap = Heap()

def addMsg(item):
    with lock:
        heap.addMessage(item)

def notifyMsgs(loop):
    with lock:
        # print(heap)
        time.sleep(1)
        for i in heap.heap:
            if not i.is_empty():
                future = asyncio.run_coroutine_threadsafe(i.send(), loop)
                future.result()

def while_loop(loop):
    while True:
        if not heap.isEmpty():
            print(heap)
            now = datetime.now()
            minMessage = heap.top()
            minMessageTime = minMessage.time
            if now - minMessageTime > timedelta(minutes=5):
                if not heap.isEmpty() and not heap.top().is_empty():
                    future = asyncio.run_coroutine_threadsafe(heap.top().send(), loop)
                    future.result()
                    break
            time.sleep(5)


