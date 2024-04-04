from telethon import TelegramClient, events
import asyncio
import sys
from main import *
from MainBot.testBox import heap

from telethon.errors import SessionPasswordNeededError
import time
from Message import Message
# import myData

import MainBot.handler as mainbot
import datetime


# API_ID = myData.API_ID
# API_HASH = myData.API_HASH
# PASSWORD = myData.PASSWORD
# PHONE_NUMBER = myData.PHONE_NUMBER

def get_name():
    return str((datetime.datetime.now() - datetime.datetime(2021,1,1)).total_seconds()) + ".session"

class TgClient:

    def __init__(self, api_id, api_hash, name="anon"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.name = name

        # self.subscribed_users = ["olivka_050, me"]
        self.subscribed_users = []
        self.client = TelegramClient(get_name(), self.api_id, self.api_hash)
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
            to_username = None
            if hasattr(to, 'username') and to.username:
                to_username = to.username

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
                if timeDeltaSeconds > 3600 and not self.hasUniqueMessage:
                    print("Пауза")
                    message: Message.MessageOnce = await self.createMessage(sender_id)
                    if not self.hasUniqueMessage:
                        self.addToHeap(message)

            elif sender_id == self.client._self_id and to_username in self.subscribed_users:
                if self.hasUniqueMessage:
                    self.removeFromHeap(sender_id, to_username, "once")

    async def createMessage(self, sender_id):
        context = await self.client.get_messages(sender_id, limit=self.numberOfMessagesInContext)
        contextList = []
        for message in context:
            contextList.append(message.raw_text)
        message = Message.MessageOnce(contextList)
        return message

    async def manageInputCode(self):
        print("Был запрошен код подтверждения")
        # await MainBot.MainBot.manageInputCode
        code = input("Введите код подтверждения: ")
        return code

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

    async def run(self):
        if not self.phone or not self.password or not self.code:
            return 1
        try:
            if not self.client.is_connected():
                await self.client.connect()
            if not await self.client.is_user_authorized():
                print("trying")
                await self.client.sign_in(phone=self.phone, code=self.code, password=self.password)
                await self.client.run_until_disconnected()
                print("after start")
            return 0
        except Exception as e:
            print("run ", e)
        print("Запущен")
        return 0

    async def send_message(self, username, message):
        print("send_message ", message)
        await self.client.send_message(username, message)

    def subscribe_user(self, userName):
        self.subscribed_users.append(userName)
        print(f"User {userName} has been subscribed to {self.name}")

    def addToHeap(self, message):
        heap.addMessage(message)
        self.hasUniqueMessage = True
        pass

    def removeFromHeap(self, user, subscribedUser):
        heap.delMessage(user, subscribedUser)
        self.hasUniqueMessage = False
        print(f"Message from {subscribedUser} has been removed from heap")

    def unsubscribeUser(self, tgID):
        self.subscribed_users.remove(tgID)
        self.hasUniqueMessage = False
        heap.delMessages(tgID)

