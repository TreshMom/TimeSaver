from abc import ABC, abstractmethod
from datetime import *
from typing import Dict
from template_gen import *


class Message(ABC):
    def __init__(self, context, to: str, text_to_reply: str):
        self.from_ = context
        self.to: str = to
        self.to_reply: str = text_to_reply
        self.empty = False

    @abstractmethod
    def send(self):
        pass

    def is_empty(self):
        return self.empty
    
    @abstractmethod
    def can_send(self):
        return True
    
    @abstractmethod
    def update(self):
        pass

    def __str__(self) -> str:
        return self.to_reply
    
    def __lt__(self, other):
        return self.closest_time_to_send < other.closest_time_to_send


class MessageSchedule(Message):
    def __init__(self, period: timedelta, start: datetime,  *args, **kwars):
        super().__init__(*args, **kwars)
        self.period = period
        self.start = start
        self.closest_time_to_send = start

    async def send(self):
        #if self.closest_time_to_send <= datetime.now():
        await self.from_.send_message(self.to, self.to_reply)
        self.closest_time_to_send = self.set_new_time()

    def set_new_time(self):
        return self.closest_time_to_send + self.period

    def can_send(self):
        return self.closest_time_to_send <= datetime.now()
    
    def update(self):
        self.closest_time_to_send = self.set_new_time()

    def __str__(self) -> str:
        return self.to_reply

    def __lt__(self, other):
        return self.closest_time_to_send.replace(tzinfo=timezone.utc) < other.closest_time_to_send.replace(tzinfo=timezone.utc)


class MessageOnce(Message):
    def __init__(self, time_to_send: datetime, *args, **kwars):
        super().__init__(*args, **kwars)
        self.closest_time_to_send = time_to_send

    def __lt__(self, other):
        return self.closest_time_to_send.replace(tzinfo=timezone.utc) < other.closest_time_to_send.replace(tzinfo=timezone.utc)

    async def send(self):
        self.create_text()
        await self.from_.send_message(self.to, self.text)
        self.from_.hasUniqueMessage[self.to] = False

    def can_send(self):
        return self.closest_time_to_send.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc)
    
    def update(self):
        self.empty = True

    def create_text(self):
        try:
            self.text = generate_text(self.to_reply)
        except Exception as e:
            print(e)
            return -1
        
    def __str__(self) -> str:
        return super().__str__()
    
    def get_time(self):
        return self.closest_time_to_send


def generate_text(prev_msg: str):
    ans = generate_template(prev_msg)
    print(f"Сгенерировался текст {ans}")
    return ans
