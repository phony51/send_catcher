from functools import cached_property
from pathlib import Path
from typing import ClassVar, Optional
from telethon import TelegramClient

from config.base import CamelCaseBaseModel
from telethon.network import ConnectionTcpAbridged

from config.dc import DC

SESSIONS_DIR = 'sessions'


class Client(CamelCaseBaseModel):
    _session_path: ClassVar[Path]
    api_id: int
    api_hash: str
    phone: str
    password: Optional[str] = None
    dc: Optional[DC] = None

    @cached_property
    def client(self):
        cl = TelegramClient(
            session=self._session_path,
            api_id=self.api_id,
            api_hash=self.api_hash,
            connection=ConnectionTcpAbridged
        )
        if self.dc is not None:
            cl.session.set_dc(self.dc.id, self.dc.ip, self.dc.port)
        return cl


class CatcherClient(Client):
    _session_path = Path().joinpath(SESSIONS_DIR, 'catcher')


class ProxyClient(Client):
    _session_path = Path().joinpath(SESSIONS_DIR, 'proxy')


class Clients(CamelCaseBaseModel):
    catcher: Optional[CatcherClient] = None
    proxy: Optional[ProxyClient] = None
