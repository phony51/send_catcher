from functools import cached_property
import os
from pathlib import Path
from typing import Callable, ClassVar, Optional
from telethon import TelegramClient
from config.base import CamelCaseBaseModel
from telethon.network import ConnectionTcpAbridged


class ClientConfig(CamelCaseBaseModel):
    api_id: int
    api_hash: str
    phone: str
    session_path: Path

    @cached_property
    def client(self):
        return TelegramClient(
            session=self.session_path,
            api_id=self.api_id,
            api_hash=self.api_hash,
            connection=ConnectionTcpAbridged,

            system_version="4.16.30-vxCUSTOM",
            system_lang_code='en',
            device_model='Redmi Redmi Note 11',
            app_version='Telegram Web'
        )

    async def is_authorized(self):
        def bypass_enter():
            raise ValueError('Not authorized')

        try:
            async with await self.client.start(phone=bypass_enter, password=bypass_enter, code_callback=bypass_enter):
                return True
        except ValueError:
            return False

    async def create_client_session(self, code_callback: Callable[[], str]):
        if not self.is_authorized():
            async with await self.client.start(self.phone, code_callback=code_callback):
                ...


class ProxyClientConfig(ClientConfig):
    @cached_property
    def client(self):
        return TelegramClient(
            session=self.session_path,
            api_id=self.api_id,
            api_hash=self.api_hash,
            connection=ConnectionTcpAbridged,
            receive_updates=False,

        )


class ClientsConfig(CamelCaseBaseModel):
    catcher: Optional[ClientConfig] = None
    proxy: Optional[ProxyClientConfig] = None
    CATCHER_SESSION_FILENAME: ClassVar[str] = 'catcher'
    PROXY_SESSION_FILENAME: ClassVar[str] = 'proxy'

    def remove_catcher_client(self, root_dir: Path):
        if os.path.exists(path := root_dir / f'{self.catcher.session_path}.session'):
            os.remove(path)
        self.catcher = None

    def remove_proxy_client(self, root_dir: Path):
        if os.path.exists(path := root_dir / f'{self.proxy.session_path}.session'):
            os.remove(path)
        self.proxy = None

    def add_catcher_client(self, client: ClientConfig, hard: bool = False):
        if self.catcher is None or hard:
            self.catcher = client
        else:
            raise ValueError('Catcher client already exists')

    def add_proxy_client(self, client: ProxyClientConfig, hard: bool = False):
        if self.proxy is None or hard:
            self.proxy = client
        else:
            raise ValueError('Proxy client already exists')
