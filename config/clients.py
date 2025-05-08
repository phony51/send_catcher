import os
from pathlib import Path
from typing import Callable, ClassVar, Optional
from telethon import TelegramClient
from config.base import CamelCaseBaseModel


class ClientConfig(CamelCaseBaseModel):
    api_id: int
    api_hash: str
    phone: str
    session_path: Path

    @property
    def client(self):
        return TelegramClient(
            session=self.session_path,
            api_id=self.api_id,
            api_hash=self.api_hash
        )

    async def create_client_session(self, code_callback: Callable[[], str]):
        if not self.client.is_user_authorized():
            await self.client.start(self.phone, code_callback=code_callback)
            await self.client.disconnect()


class ClientsConfig(CamelCaseBaseModel):
    catcher: Optional[ClientConfig] = None
    proxy: list[ClientConfig] = []
    CATCHER_SESSION_FILENAME: ClassVar[str] = 'catcher'

    @property
    def next_proxy_session_filename(self):
        return f'proxy-{len(self.proxy)+1}'

    def remove_catcher_client(self, root_dir: Path):
        if os.path.exists(path := root_dir / f'{self.catcher.session_path}.session'):
            os.remove(path)
        self.catcher = None

    def _find_proxy_client(self, func: Callable[[ClientConfig], bool]):
        for i in range(len(self.proxy)):
            if func(self.proxy[i]):
                return i

    def remove_proxy_client(self, root_dir: Path, func: Callable[[ClientConfig], bool]):
        if (i := self._find_proxy_client(func)) is None:
            return False
        if os.path.exists(path := root_dir / f'{self.proxy[i].session_path}.session'):
            os.remove(path)

        self.proxy.pop(i)
        return True

    def add_catcher_client(self, client: ClientConfig, hard: bool = False):
        if self.catcher is None or hard:
            self.catcher = client
        else:
            raise ValueError('Catcher client already exists')

    def add_proxy_client(self, client: ClientConfig):
        self.proxy.append(client)
