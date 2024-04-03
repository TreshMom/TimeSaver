from abc import ABC, abstractmethod
from datetime import *
from typing import Dict


class Message(ABC):
    def __init__(self, context, to: str, text_to_reply: str):
        self.from_ = context
        self.to: str = to
        self.to_reply: str = text_to_reply
        self.closest_time_to_send: datetime = None
        self.empty = False

    @abstractmethod
    def send(self):
        pass

    def get_time(self):
        return self.closest_time_to_send

    def is_empty(self):
        return self.empty


class MessageSchedule(Message):
    def __init__(self, text, json_sheduler_info : Dict[int,Dict[int, str]]):
        #  json_sheduler_info:
        #  json_sheduler_info = day -> hour -> text_to_reply[string]
        #
        self.info_scheduler = json_sheduler_info
        self.text = text
        super().__init__()

    async def send(self):
        await self.from_.send_message(self.to, self.text)
        day_now = datetime.day
        hour_now = datetime.hour
        self.closest_time_to_send = self.set_new_time()
        self.empty = False

    def set_new_time(self):
        return datetime

    def __str__(self) -> str:
        return self.text


class MessageOnce(Message):
    def __init__(self, time_to_send: datetime, *args, **kwars):
        super().__init__(*args, **kwars)
        self.closest_time_to_send = time_to_send

    async def send(self):
        self.create_text()
        await self.from_.send_message(self.to, self.text)
        self.empty = True

    def create_text(self):
        try:
            self.text = generate_text(self.to_reply)
        except Exception as e:
            print(e)
            return -1


def generate_text(prev_msg: str):
    return "Tolik"
