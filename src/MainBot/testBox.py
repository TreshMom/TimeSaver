import threading
import time as t
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
        t.sleep(1)
        for i in heap.heap:
            if not i.is_empty():
                future = asyncio.run_coroutine_threadsafe(i.send(), loop)
                future.result()


def while_loop(loop):
    while True:
        now = datetime.now()
        try:
            minMessage = heap.heap[0]
            minMessageTime = minMessage.time
            if now - minMessageTime > timedelta(minutes=5):
                if not heap.heap[0].is_empty():
                    future = asyncio.run_coroutine_threadsafe(heap.heap[0].send(), loop)
                    future.result()
                    break
            t.sleep(5)
        except Exception as e:
            print("Вероятно, куча пустая")
            t.sleep(5)


