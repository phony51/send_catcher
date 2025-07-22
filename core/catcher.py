import logging
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import User, InputPeerUser


def filter_(msg: Message):
    return msg.buttons is not None \
        and msg.buttons[0][0].url is not None \
        and msg.buttons[0][0].url[23:25] == 'CQ'


class ChequeProcessor:
    __start_text = '/start '

    def __init__(self, domain: str, cryptobot: User, client: TelegramClient):
        self.domain = domain
        self.cryptobot = InputPeerUser(cryptobot.id, cryptobot.access_hash)
        self._client = client
        self._logger = logging.getLogger(__name__)

    async def _activate_cheque(self, cheque_id: str):
        await self._client(SendMessageRequest(peer=self.cryptobot, message=self.__start_text + cheque_id))

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
                func=filter_))
            self.client.add_event_handler(self.cheque_processor.handler, events.NewMessage(
                func=filter_))
            await self.client.run_until_disconnected()
