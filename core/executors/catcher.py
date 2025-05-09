import logging
import re
from telethon import TelegramClient, events, errors
from core.clients_pool import ClientsPool
from telethon.tl.custom.message import Message


class ChequeProcessor:

    def __init__(self, domain: str, bot_id: int, clients_pool: ClientsPool, cheque_id_regex: re.Pattern):
        self.domain = domain
        self.bot_id = bot_id
        self._clients_pool = clients_pool
        self.cheque_id_regex = cheque_id_regex
        self._logger = logging.getLogger(__name__)

    async def ready(self):
        await self._clients_pool.ready()
        
    async def _activate_cheque(self, cheque_id: str):
        text = f'/start {cheque_id}'
        try:
            await self._clients_pool.current_client.send_message(self.domain, text)
        except errors.FloodWaitError as fwe:
            prev_api_id = self._clients_pool.current_client.api_id
            await self._clients_pool.switch()
            self._logger.warning(
                f'Client {prev_api_id} has cooldown for {fwe.seconds} seconds. Switched to {self._clients_pool.current_client.api_id}')
            await self._clients_pool.current_client.send_message(self.domain, text)
        finally:
            self._logger.info('Activating cheque...')

    def filter_(self, msg: Message) -> bool:
        return msg.via_bot_id is not None \
            and msg.buttons is not None \
            and msg.via_bot_id == self.bot_id \
            and (url := msg.buttons[0][0].url) \
            and url[23] == 'C' and url[24] == 'Q'

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
