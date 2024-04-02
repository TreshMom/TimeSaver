from telethon import TelegramClient, events
import asyncio
import sys
from main import *

from telethon.errors import SessionPasswordNeededError
import time
from Message import Message
import myData

# API_ID = myData.API_ID
# API_HASH = myData.API_HASH
# PASSWORD = myData.PASSWORD
# PHONE_NUMBER = myData.PHONE_NUMBER


class TgClient:

    def __init__(self, api_id, api_hash, name="anon"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.name = name
        #self.subscribed_users = ["olivka_050, me"]
        self.subscribed_users = []
        self.client = TelegramClient('anon', self.api_id, self.api_hash)
        self.hasUniqueMessage = False

        self.numberOfMessagesInContext = 10

        @self.client.on(events.MessageEdited)
        async def handler(event):
            sender = await event.get_sender()
            sender_id = sender.id
            sender_username = sender.username

            if sender_username in self.subscribed_users:
                await self.client.send_message(sender_id, "Хули редактируешь")

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

    async def getPhoneNumber(self):
        # phone = await mainBot.getPhoneNumber()
        phone = "89213830029"
        return phone


    async def getPassword(self):
        # password = await mainBot.getPassword()
        password = "Mam190572"
        return password


    async def run(self):
        await self.client.start(password=self.getPassword, phone=self.getPhoneNumber, code_callback=self.manageInputCode)
        print("Запущен")


    async def send_message(self, username, message):
        print("send_message ", message)
        if username in self.subscribed_users:
            await self.client.send_message(username, message)


    def subscribe_user(self, userName):
        self.subscribed_users.append(userName)
        print(f"User {userName} has been subscribed to {self.name}")

    def addToHeap(self, message):
        # heap.insertMessage(self)
        self.hasUniqueMessage = True
        pass

    def removeFromHeap(self, user, subscribedUser, typeOfMessage = "once"):
        # heap.deleteMessageFromUser(user, subscribedUser, typeOfMessage)
        self.hasUniqueMessage = False
        print(f"Message from {subscribedUser} has been removed from heap")
        pass

    def unsubscribeUser(self, userName):
        self.subscribed_users.remove(userName)
        pass


if __name__ == "__main__":
    cl = TgClient(API_ID, API_HASH)
    cl.run()
