import json
from datetime import datetime
import NewsLoader
import NewsSender
from bot import RapidNewsBot
import time
import asyncio


async def runBot():
    await RapidNewsBot.main()


asyncio.run(runBot())








































"""
class MessageQueue:
    __queue = asyncio.Queue()

    @staticmethod
    async def enqueue(self, message):
        await self.__queue.put(message)

    @staticmethod
    async def dequeue(self):
        return await self.__queue.get()

    @staticmethod
    def is_empty(self):
        return self.__queue.empty()
"""




