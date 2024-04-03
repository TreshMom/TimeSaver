from abc import ABC, abstractmethod
from datetime import *


class Message(ABC):
    def __init__(self, context, to: str, text_to_replt: str):
        self.from_ = context
        self.to: str = to
        self.to_reply: str = text_to_replt
        self.closest_time_to_send: datetime = None
        self.empty = True

    @abstractmethod
    def send(self):
        pass

    def get_time(self):
        return self.closest_time_to_send

    def is_empty(self):
        return True


class MessageSchedule(Message):
    def __init__(self, text):
        self.text = text
        super().__init__()

    async def send(self):
        self.from_.send_message(self.to, self.text)
        self.closest_time_to_send = await self.set_new_time()
        self.empty = False

    async def set_new_time(self):
        return datetime

    def __str__(self) -> str:
        return self.text
        # return super().__str__()


class MessageOnce(Message):
    def __init__(self, time_to_send: datetime, *args, **kwars):
        super().__init__(*args, **kwars)
        self.closest_time_to_send = time_to_send

    async def send(self):
        print(" i send to ")
        self.create_text()
        await self.from_.send_message(self.to, self.text)
        self.empty = False

    def create_text(self):
        try:
            self.text = generate_text(self.to_reply)
        except Exception as e:
            print(e)
            return -1


def generate_text(prev_msg: str):
    return "Tolik"
