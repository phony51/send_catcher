import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import re
from telethon import TelegramClient, events, errors
from core.clients_pool import ClientsPool
from telethon.tl.custom.message import Message


class ChequeProcessor:
    __start_text = '/start '
    def __init__(self, domain: str, bot_id: int, clients_pool: ClientsPool, filter_max_workers: int, activation_max_workers: int, cheque_id_regex: re.Pattern):
        self.domain = domain
        self.bot_id = bot_id
        self._clients_pool = clients_pool
        self.cheque_id_regex = cheque_id_regex
        self._logger = logging.getLogger(__name__)
        self.filter_executor = ThreadPoolExecutor(max_workers=filter_max_workers)
        self.activation_executor = ThreadPoolExecutor(max_workers=activation_max_workers)
    
    async def ready(self):
        await self._clients_pool.ready()
        
    async def handler(self, event):
        # Быстрая проверка фильтра в отдельном потоке
        if not await self._run_filter(event):
            return
            
        # Обработка активации чека в другом потоке
        await self._process_activation(event)
    
    async def _run_filter(self, event):
        # Выносим CPU-bound фильтрацию в отдельный поток
        return await asyncio.get_event_loop().run_in_executor(
            self.filter_executor,
            self.filter_,
            event
        )
    
    async def _process_activation(self, event):
        # Выносим IO-bound активацию в отдельный поток
        cheque_id = self._extract_cheque_id(event)
        await asyncio.get_event_loop().run_in_executor(
            self.activation_executor,
            lambda: asyncio.run_coroutine_threadsafe(
                self._activate_cheque(cheque_id),
                asyncio.get_event_loop()
            ).result()
        )
    
    def _extract_cheque_id(self, msg):
        # Извлекаем ID чека из URL кнопки
        url = msg.buttons[0][0].url
        return url.split('/')[-1]  # Предполагаем формат URL
    
    def filter_(self, msg):
        # Ваш существующий фильтр без изменений
        return msg.via_bot_id is not None \
            and msg.buttons is not None \
            and msg.via_bot_id == self.bot_id \
            and (url := msg.buttons[0][0].url) \
            and url[23] == 'C' and url[24] == 'Q'
    
    async def _activate_cheque(self, cheque_id: str):
        # Ваш существующий метод активации без изменений
        try:
            await self._clients_pool.current_client.send_message(self.domain, self.__start_text + cheque_id)
        except errors.FloodWaitError as fwe:
            prev_api_id = self._clients_pool.current_client.api_id
            await self._clients_pool.switch()
            self._logger.warning(
                f'Client {prev_api_id} has cooldown for {fwe.seconds} seconds. Switched to {self._clients_pool.current_client.api_id}')
            await self._clients_pool.current_client.send_message(self.domain, self.__start_text + cheque_id)
        finally:
            self._logger.info('Activating cheque...')

    async def handler(self, msg: Message):
        await self._activate_cheque(msg.buttons[0][0].url[23:])


class CatcherLoop:
    def __init__(self, client: TelegramClient, cheque_processor: ChequeProcessor):
        self.client = client
        self.cheque_processor = cheque_processor

    async def run(self):
        logging.info('Loop started')
        await self.cheque_processor.ready()
        async with await self.client.start():
            self.client.add_event_handler(self.cheque_processor.handler, events.MessageEdited(
                func=self.cheque_processor.filter_))
            self.client.add_event_handler(self.cheque_processor.handler, events.NewMessage(
                func=self.cheque_processor.filter_))
            await self.client.run_until_disconnected()
