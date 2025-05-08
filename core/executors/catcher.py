import logging
import re
from telethon import TelegramClient, events, errors
from core.clients_pool import ClientsPool
from telethon.tl.custom.message import Message
# import timeit
# from functools import wraps


# def measure_time(func):
#     @wraps(func)
#     async def async_wrapper(*args, **kwargs):
#         start_time = timeit.default_timer()
#         try:
#             return await func(*args, **kwargs)
#         finally:
#             elapsed = (timeit.default_timer() - start_time)   # в миллисекундах
#             print(f"⏱ {func.__name__} took {elapsed:.2f}us")

    # return async_wrapper


class ChequeProcessor:

    def __init__(self, domain: str, bot_id: int, clients_pool: ClientsPool, cheque_id_regex: re.Pattern):
        self.domain = domain
        self.bot_id = bot_id
        self._clients_pool = clients_pool
        self.cheque_id_regex = cheque_id_regex
        self._logger = logging.getLogger(__name__)

    async def _activate_cheque(self, cheque_id: str):
        coro = self._clients_pool.current_client.send_message(self.domain, f'/start {cheque_id}')
        try:
            await coro
        except errors.FloodWaitError as fwe:
            self._clients_pool.switch()
            self._logger.warning(f'Client {self._clients_pool.current_client._phone} has cooldown for {fwe.seconds} seconds. Switching...')
            await coro
        finally:
            self._logger.info('Activating cheque...')
        

    def filter_(self, msg: Message) -> bool: 
        return msg.via_bot_id == self.bot_id \
                and msg.buttons is not None \
                and (url := msg.buttons[0][0].url) \
                and url[23:25] == 'CQ'
        
    async def handler(self, msg: Message):
        await self._activate_cheque(msg.raw_text[23:])


class CatcherLoop:
    def __init__(self, cheque_processor: ChequeProcessor):
        self.cheque_processor = cheque_processor
        
    async def run(self, catcher_client: TelegramClient):
        catcher_client.add_event_handler(self.cheque_processor.handler, events.MessageEdited(func=self.cheque_processor.filter_))
        catcher_client.add_event_handler(self.cheque_processor.handler, events.NewMessage(func=self.cheque_processor.filter_))
        await catcher_client.run_until_disconnected()
