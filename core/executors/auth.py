from telethon import TelegramClient
from core.executors.executor import ClientExecutor


class AuthExecutor(ClientExecutor):

    async def execute_by(self, client: TelegramClient, phone: str):
        await client.connect()
        await client.start(phone, None if await client.is_user_authorized() else input(f'Enter verification code ({phone})'))
        await client.get_me()
