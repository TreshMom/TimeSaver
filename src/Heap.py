import heapq
import Message

class Heap:

    def __init__(self):
        self.heap = []
        heapq.heapify(self.heap)

    def addMessage(self, message: Message):
        # в приоритет наверное нужно запихать (текущее время - время сообщения)
        heapq.heappush(self.heap, (message.priority, message))

    def send(self, message: Message):
        for i, val in enumerate(self.heap):
            if val.fromm == message.fromm and val.to == message.to and val.text == message.text:
                self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                break
        message.send()
        self.heap.pop()
        heapq.heapify(self.heap)

    def send(self):
        message = heapq.heappop(self.heap)
        message.send()
    
    def delMessage(self, message: Message):
        for i, val in enumerate(self.heap):
            if val.fromm == message.fromm and val.to == message.to and val.text == message.text:
                self.heap[i], self.heap[-1] = self.heap[-1], self.heap[i]
                break
        self.heap.pop()
        heapq.heapify(self.heap)

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
        pass
