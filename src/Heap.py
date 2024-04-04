from datetime import datetime, timedelta
import time
import asyncio
import time as t

import heapq
from Message import *
import threading
from datetime import datetime, timezone 

class Heap:

    def __init__(self):
        self.lock = threading.Lock()
        with self.lock:
            self.heap = []
            heapq.heapify(self.heap)

    def addMessage(self, message: Message):
        print("before lock")
        with self.lock:
            print("after lock")
            heapq.heappush(self.heap, message)
            print("Сообщение добавлено в кучу")
            print("размер кучи", len(self.heap))
            print("сама куча", self.heap)

    # def send(self, message: Message):
    #     for i, val in enumerate(self.heap):
    #         if val.fromm == message.fromm and val.to == message.to and val.text == message.text and val.time == message.time:
    #             self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
    #             break
    #     message.send()
    #     heapq.heappop(self.heap)
    
    def delMessage(self, fromm, to):
        with self.lock:
            print("def delMessage(self, fromm, to):")
            for i, val in enumerate(self.heap):
                if val.fromm == fromm and val.to == to and isinstance(val, MessageSchedule):
                    self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                    break
            self.heap.pop()
            heapq.heapify(self.heap)

    def delMessages(self, tgID):
        with self.lock:
            print("def delMessages(self, tgID):")
            def removeByIndices(array: list, indices: list):
                indices.sort(reverse=True)
                for index in indices:
                    del array[index]
                return array
            indices = []
            for i, val in enumerate(self.heap):
                if val.fromm == tgID:
                    indices.append(i)
            self.heap = removeByIndices(self.heap, indices)
            heapq.heapify(self.heap)

    def isEmpty(self):
        return not bool(self.heap)
    
    def top(self):
        """
        Check if heap is empty before usage
        """
        return self.heap[0]

    def run(self, loop):
        print("Куча запущена")
        while True:
            try:
                with self.lock:
                    if len(self.heap) == 0:
                        # print(" куча пустая ")
                        t.sleep(0.5)
                        continue

                    minMessage = self.top()
                    # print("after lock run(self, loop)")
                    # удаляем сообщение из головы 
                    if minMessage.can_send():
                        heapq.heappop(self.heap)

                        minMessage.update()

                        future = asyncio.run_coroutine_threadsafe(minMessage.send(), loop)
                        # future.result()
                        # print("Сообщение из кучи добавлено в эвент луп главного потока")

                        if not minMessage.is_empty():
                            heapq.heappush(self.heap, minMessage)
                        # print("сообщения :", self.heap)
                t.sleep(0.5)
            except Exception as e:
                print("Вероятно, куча пустая")
                print(e)
                t.sleep(5)

heap = Heap()

# ioloop = asyncio.new_event_loop()
# hp = Heap()
# if __name__ == '__main__':
#     print("fd")
#     thread1 = threading.Thread(target=hp.run, args=(ioloop,))
#     thread1.daemon = True
#     thread1.start()

#     t.sleep(4)

#     hp.addMessage(MessageOnce(datetime.now() + timedelta(seconds=5), "fdsfds", "fsdfsdf", "fdsf"))
#     hp.addMessage(MessageOnce(datetime.now() + timedelta(seconds=5), "fdsfds", "fsdfsdf", "fdsf"))
#     t.sleep(20)