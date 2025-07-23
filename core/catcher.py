import logging
from telethon import TelegramClient, events
from telethon.tl import types
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import User, InputPeerUser


class Cryptobot:
    __start_text = '/start '

    def __init__(self, ent: User, client: TelegramClient):
        self.cryptobot = InputPeerUser(ent.id, ent.access_hash)
        self._client = client
        self._logger = logging.getLogger(__name__)

    async def handler(self, update: types.TypeUpdate):
        if ((update.CONSTRUCTOR_ID == types.UpdateEditChannelMessage.CONSTRUCTOR_ID or
             update.CONSTRUCTOR_ID == types.UpdateNewChannelMessage.CONSTRUCTOR_ID or
             update.CONSTRUCTOR_ID == types.UpdateNewMessage.CONSTRUCTOR_ID or
             update.CONSTRUCTOR_ID == types.UpdateEditMessage.CONSTRUCTOR_ID) and
            update.message.reply_markup is not None
            and update.message.reply_markup.rows[0].buttons[
                0].CONSTRUCTOR_ID == types.KeyboardButtonUrl.CONSTRUCTOR_ID
            and len(update.message.reply_markup.rows[0].buttons[0].url) == 35) \
                and update.message.reply_markup.rows[0].buttons[0].url[23] == 'C':
            await self._client(SendMessageRequest(peer=self.cryptobot,
                                                  message=self.__start_text + update.message.reply_markup.rows[0].
                                                  buttons[0].url[23:]))
            self._logger.info('Cheque has been caught')


class Catcher:
    def __init__(self, client: TelegramClient, cryptobot: Cryptobot):
        self.client = client
        self._cryptobot = cryptobot

    async def run(self):
        logging.info('Catcher started')
        async with await self.client.start():
            self.client.on(events.Raw())(self._cryptobot.handler)
            await self.client.run_until_disconnected()
