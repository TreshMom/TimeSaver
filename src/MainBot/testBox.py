import threading
import time
import asyncio
from datetime import datetime, timedelta
import Heap

lock = threading.Lock()
heap = Heap()

def addMsg(item):
    with lock:
        shared_list.append(item)

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
        now = datetime.now()
        minMessage = heap.heap[0]
        minMessageTime = minMessage.time
        if now - minMessageTime > timedelta(minutes=5):
            if not heap.heap[0].is_empty():
                future = asyncio.run_coroutine_threadsafe(heap.heap[0].send(), loop)
                future.result()
                break
        time.sleep(5)


