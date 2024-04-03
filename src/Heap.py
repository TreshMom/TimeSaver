from datetime import datetime, timedelta
import time
import asyncio
import time as t

import heapq
from Message import *

class Heap:

    def __init__(self):
        self.heap = []
        heapq.heapify(self.heap)

    def addMessage(self, message: Message):
        heapq.heappush(self.heap, message)

    def send(self, message: Message):
        for i, val in enumerate(self.heap):
            if val.fromm == message.fromm and val.to == message.to and val.text == message.text and val.time == message.time:
                self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                break
        message.send()
        heapq.heappop(self.heap)

    def send(self):
        message = heapq.heappop(self.heap)
        message.send()
    
    def delMessage(self, fromm, to):
        for i, val in enumerate(self.heap):
            if val.fromm == fromm and val.to == to and isinstance(val, MessageSchedule):
                self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                break
        heapq.heappop(self.heap)

    def delMessages(self, tgID):
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

    def run(self):
        print("Куча запущена")
        while True:
            if not self.isEmpty():
                now = datetime.now()
                try:
                    minMessage = self.top()
                    minMessageTime = minMessage.time
                    if now - minMessageTime > timedelta(minutes=5):
                        self.send()
                        break
                    time.sleep(5)
                except Exception as e:
                    print("Вероятно, куча пустая")
                    t.sleep(5)

