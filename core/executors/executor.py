from abc import ABC, abstractmethod

from telethon import TelegramClient
from telethon.tl.custom.message import Message


class ClientExecutor(ABC):
    """Абстракция для запуска клиента с определенной логикой"""
    @abstractmethod
    async def execute_by(self, client: TelegramClient, *args):
        pass


class MessageProcessor(ABC):
    """Абстракция для обработки сообщений"""
    @abstractmethod
    async def process(self, message: Message) -> bool:
        pass
