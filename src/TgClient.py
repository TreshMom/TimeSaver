from telethon import TelegramClient, events
import asyncio
import sys
from main import *

from MainBot.testBox import heap
import Heap
import telethon


from telethon.errors import SessionPasswordNeededError
import time

from Message import *
import MainBot.handler as mainbot
import datetime


def get_name():
    return str((datetime.datetime.now() - datetime.datetime(2021,1,1)).total_seconds()) + ".session"

class TgClient:

    def __init__(self, api_id, api_hash, name="anon"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.name = name

        self.subscribed_users = []
        self.client = TelegramClient(get_name(), self.api_id, self.api_hash, device_model="My MAC", system_version="10.15.7", app_version="0.0.1", lang_code="en")
        self.hasUniqueMessage = False
        self.phone = None
        self.password = None
        self.code = None


        @self.client.on(events.NewMessage)
        async def handler(event):
            sender = await event.get_sender()
            sender_id = sender.id
            sender_username = sender.username
            to = await event.get_chat()
            to_id = to.id
            to_username = None
            print(f"ПОЛУЧЕНО СООБЩЕНИЕ от {sender_username}")


            if sender_username in self.subscribed_users:
                print(f"Received a message from {sender_username or sender_id}: {event.raw_text}")

                timeOfMessage = event.date
                lastMyMessage = None
                lastMessages = await self.client.get_messages(sender_id, limit=100)
                for msg in lastMessages:
                    fromm = await msg.get_sender()
                    if fromm.id == self.client._self_id:
                        lastMyMessage = msg
                        break
                lastMyMessageDate = lastMyMessage.date
                timeDelta = timeOfMessage - lastMyMessageDate
                timeDeltaSeconds = timeDelta.total_seconds()
                print(f"timeDeltaSeconds {timeDeltaSeconds}")
                if timeDeltaSeconds > 10 and not self.hasUniqueMessage:
                    timeToSend = timeOfMessage + datetime.timedelta(seconds=10)
                    message: MessageOnce = await self.createMessage(self.client._self_id, sender_id, event.raw_text, timeOfMessage, timeToSend)
                    if not self.hasUniqueMessage:
                        self.addToHeap(message)

            elif sender_id == self.client._self_id and to_username in self.subscribed_users:
                if self.hasUniqueMessage:
                    self.removeFromHeap(sender_id, to_id)

    async def createMessage(self, fromm, to, text, time, timeToSend):
        context = text
        message = MessageOnce(fromm, to, context, time, timeToSend)
        return message


    def set_phone_password(self, phone, password):
        self.phone = phone
        self.password = password
        print("set_phone_and_password")
        print(self.phone)

    
    def set_code(self, code):
        self.code = code

    async def send_code_request(self):
        if not self.client.is_connected():
                await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)


    def get_phone(self):
        return self.phone

    def get_password(self):
        return self.password

    def get_code(self):
        return self.code

    async def run(self):
        if not self.phone or not self.password or not self.code:
            print("no phone or password or code")
            return 1
        try:
            if not self.client.is_connected():
                print("connecting")
                await self.client.connect()
            if not await self.client.is_user_authorized():
                print("trying")
                try:
                    await self.client.sign_in(phone=self.phone, code=self.code)
                except telethon.errors.SessionPasswordNeededError:
                    await self.client.sign_in(password=self.password)
                print("Запущен")
                await self.client.run_until_disconnected()
                print("after start")
            return 0
        except Exception as e:
            print("Произошла ошибка запуска бота ", e)
        return 0

    async def send_message(self, username, message):
        print("send_message ", message)
        await self.client.send_message(username, message)

    def subscribe_user(self, userName):
        userName = userName.lstrip("@")
        self.subscribed_users.append(userName)
        print(f"User {userName} has been subscribed to {self.name}")
        print(self.subscribed_users)

    def addToHeap(self, message):
        heap.addMessage(message)
        self.hasUniqueMessage = True
        pass

    def removeFromHeap(self, userId, subscribedUser):
        heap.delMessage(userId, subscribedUser)
        self.hasUniqueMessage = False
        print(f"Message from {subscribedUser} has been removed from heap")

    def unsubscribeUser(self, tgID):
        self.subscribed_users.remove(tgID)
        self.hasUniqueMessage = False
        heap.delMessages(tgID)

