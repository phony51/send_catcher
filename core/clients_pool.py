from telethon import TelegramClient


class ClientsPool:
    _clients: list[TelegramClient]
    _current_client_index: int = 0

    def __init__(self, clients: list[TelegramClient]):
        if len(self._clients) == 0:
            raise ValueError('Not enough executors')
        self._clients = clients

    @property
    def current_client(self):
        return self._clients[self._current_client_index]

    def switch(self):
        if self._current_client_index == len(self._clients) - 1:
            self._current_client_index = 0
        else:
            self._current_client_index += 1
        
