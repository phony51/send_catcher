from telethon import TelegramClient
from core.executors.executor import ClientExecutor


class ProxyExecutor(ClientExecutor):
    """Просто поддерживает соединение прокси-клиента"""

    async def execute_by(self, client: TelegramClient):
        await client.run_until_disconnected()
