import logging
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.types import User


class ChequeProcessor:
    __start_text = '/start '

    def __init__(self, domain: str, cryptobot: User, client: TelegramClient):
        self.domain = domain
        self.cryptobot = cryptobot
        self._client = client
        self._logger = logging.getLogger(__name__)

    def filter_(self, msg: Message):
        return msg.via_bot_id is not None \
            and msg.buttons is not None \
            and msg.via_bot_id == self.cryptobot.id \
            and msg.buttons[0][0].url is not None \
            and msg.buttons[0][0].url[23:25] == 'CQ'

    async def _activate_cheque(self, cheque_id: str):
        async with self._client:
            await self._client.send_message(self.cryptobot, self.__start_text + cheque_id)

    async def handler(self, msg: Message):
        await self._activate_cheque(msg.buttons[0][0].url[23:])


class CatcherLoop:
    def __init__(self, client: TelegramClient, cheque_processor: ChequeProcessor):
        self.client = client
        self.cheque_processor = cheque_processor

    async def run(self):
        logging.info('Loop started')
        async with await self.client.start():
            self.client.add_event_handler(self.cheque_processor.handler, events.MessageEdited(
                func=self.cheque_processor.filter_))
            self.client.add_event_handler(self.cheque_processor.handler, events.NewMessage(
                func=self.cheque_processor.filter_))
            await self.client.run_until_disconnected()
