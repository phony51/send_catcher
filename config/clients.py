from functools import cached_property
from pathlib import Path
from typing import ClassVar, Optional
from telethon import TelegramClient

from config.base import CamelCaseBaseModel
from telethon.network import ConnectionTcpAbridged


SESSIONS_DIR = 'sessions'


class Client(CamelCaseBaseModel):
    _session_path: ClassVar[Path]
    api_id: int
    api_hash: str
    phone: str
    password: Optional[str] = None

    @cached_property
    def client(self):
        return TelegramClient(
            session=self._session_path,
            api_id=self.api_id,
            api_hash=self.api_hash,
            device_model="iPhone 12 mini",
            system_version='18.5',
            lang_code='en',
            system_lang_code='en',
            connection=ConnectionTcpAbridged
        )


class CatcherClient(Client):
    _session_path = Path().joinpath(SESSIONS_DIR, 'catcher')


class ProxyClient(Client):
    _session_path = Path().joinpath(SESSIONS_DIR, 'proxy')


class Clients(CamelCaseBaseModel):
    catcher: Optional[CatcherClient] = None
    proxy: Optional[ProxyClient] = None
