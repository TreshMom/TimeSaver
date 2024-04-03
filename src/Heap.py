from datetime import datetime, timedelta
import time

import heapq
import Message

class Heap:

    def __init__(self):
        self.heap = []
        heapq.heapify(self.heap)

    def addMessage(self, message: Message):
        # нужно добавить время (datetime) получения сообщения -> message.time
        # добавьте в class Message     
        # def __lt__(self, other):
        #     return self.time < other.time
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
    
    def delMessage(self, message: Message):
        for i, val in enumerate(self.heap):
            if val.fromm == message.fromm and val.to == message.to and val.text == message.text and val.time == message.time:
                self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                break
        heapq.heappop(self.heap)

    def delMessages(self, tgID: int):
        def removeByIndices(array: list, indices: list):
            indices.sort(reverse=True)
            for index in indices:
                del array[index]
            return array
        indices = []
        for i, val in enumerate(self.heap):
            if val.to == tgID:
                indices.append(i)
        self.heap = removeByIndices(self.heap, indices)
        heapq.heapify(self.heap)

    def run(self):
        while True:
            now = datetime.now()
            minMessage = self.heap[0]
            minMessageTime = minMessage.time
            if now - minMessageTime > timedelta(minutes=5):
                self.send()
                break
            time.sleep(5)
