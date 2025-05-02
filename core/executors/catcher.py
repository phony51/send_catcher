import asyncio
import logging
import re
from telethon import TelegramClient, events
from core.executors.executor import ClientExecutor, MessageProcessor
from telethon.tl.custom.message import Message
import timeit
from functools import wraps


def measure_time(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed = (timeit.default_timer() - start_time)   # в миллисекундах
            print(f"⏱ {func.__name__} took {elapsed:.2f}us")

    return async_wrapper


class ChequeProcessor(MessageProcessor):
    __slots__ = ('domain', 'bot_id', 'sender', 'cheque_id_regex')

    def __init__(self, domain: str, bot_id: int, sender: TelegramClient, cheque_id_regex: re.Pattern):
        self.domain = domain
        self.bot_id = bot_id
        self.sender = sender
        self.cheque_id_regex = cheque_id_regex
        self._logger = logging.getLogger(__name__)

    async def _activate_cheque(self, cheque_id: str):
        cmd = f'/start {cheque_id}'
        await self.sender.send_message(self.domain, cmd)
        self._logger.info('Activating cheque...')

    async def process(self, msg: Message) -> bool:
        if msg.via_bot_id == self.bot_id \
                and msg.buttons is not None \
                and (url := msg.buttons[0][0].url) \
                and url[23:25] == 'CQ':
            asyncio.create_task(self._activate_cheque(url[23:]))
            return True
        if msg.raw_text is not None and (url := self.cheque_id_regex.search(msg.raw_text)) is not None:
            asyncio.create_task(self._activate_cheque(url.group()))
            return True
        return False


class CatcherExecutor(ClientExecutor):
    def __init__(self, processor: MessageProcessor):
        self.processor = processor

    async def execute_by(self, client: TelegramClient):
        def handler(event): return self.processor.process(event.message)
        client.add_event_handler(handler, events.MessageEdited)
        client.add_event_handler(handler, events.NewMessage)
        await client.run_until_disconnected()
