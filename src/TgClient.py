from telethon import TelegramClient, events
import asyncio
import sys
from main import *

from telethon.errors import SessionPasswordNeededError

import Message
import myData

API_ID = myData.API_ID
API_HASH = myData.API_HASH
PASSWORD = myData.PASSWORD
PHONE_NUMBER = myData.PHONE_NUMBER


class TgClient:

    def __init__(self, api_id, api_hash, name="anon"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.name = name
        self.subscribed_users = ["olivka_050, me"]
        self.client = TelegramClient('anon', API_ID, API_HASH)

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

            if sender_username in self.subscribed_users:
                print(f"Received a message from {sender_username or sender_id}: {event.raw_text}")

                timeOfMessage = event.date
                timeOOfPreviousMessage = self.client.get_messages(sender_id, limit=2)[1].date
                timeDelta = timeOfMessage - timeOOfPreviousMessage
                timeDeltaSeconds = timeDelta.total_seconds()
                if timeDeltaSeconds > 3600:
                    print("Пауза")
                    message: Message.MessageOnce = await self.createMessage(sender_id)
                    self.addToHeap(message)

    async def createMessage(self, sender_id):
        context = await self.client.get_messages(sender_id, limit=self.numberOfMessagesInContext)
        contextList = []
        for message in context:
            contextList.append(message.raw_text)
        message = Message.MessageOnce(contextList)
        return message


    def manageInputCode(self):
        print("Был запрошен код подтверждения")
        # await MainBot.MainBot.manageInputCode
        code = input("Введите код подтверждения: ")
        return code


    def run(self):
        self.client.start(PHONE_NUMBER, code_callback=self.manageInputCode)

        self.client.run_until_disconnected()


    async def send_message(self, userame, message):
        text = message.text
        await self.client.send_message(userame, text)


    def subscribe_user(self, userName):
        self.subscribed_users.append(userName)
        print(f"User {userName} has been subscribed to {self.name}")

    def addToHeap(self, message):
        # heap.insertMessage(self)
        pass

    def unsubscribeUser(self, userName):
        # heap.deleteAllMessagesFromUser(tg_id)
        self.subscribed_users.remove(userName)
        pass


if __name__ == "__main__":
    cl = TgClient(API_ID, API_HASH)
    cl.run()
