import asyncio
import logging
import os
from pathlib import Path
import re
from config.app import AppConfig, load_config
from telethon import TelegramClient

from core.executors.catcher import CatcherExecutor, ChequeProcessor
from core.executors.proxy import ProxyExecutor
from core.executors.auth import AuthExecutor
from logger.logger import setup_logger


async def run(app_config: AppConfig):
    setup_logger(app_config.logger)
    proxy_client_config = app_config.clients.proxy_client
    proxy_client = TelegramClient(

        session=os.path.abspath(Path('sessions', proxy_client_config.session_name)),
        api_id=proxy_client_config.api_id,
        api_hash=proxy_client_config.api_hash
    )

    catcher_client_config = app_config.clients.catcher_client
    catcher_client = TelegramClient(
        session=os.path.abspath(Path('sessions', catcher_client_config.session_name)),
        api_id=catcher_client_config.api_id,
        api_hash=catcher_client_config.api_hash
    )
    try:
        await AuthExecutor().execute_by(proxy_client, proxy_client_config.phone)
        await AuthExecutor().execute_by(catcher_client, catcher_client_config.phone)
        logging.debug('Authorization successfully')
        cheque_processor = ChequeProcessor(
            domain=app_config.crypto_bot.domain,
            bot_id=app_config.crypto_bot.id,
            sender=proxy_client,
            cheque_id_regex=re.compile(r'CQ[A-Za-z0-9]{10}')
        )
        logging.info('Loop started')
        await asyncio.gather(
            ProxyExecutor().execute_by(proxy_client),
            CatcherExecutor(cheque_processor).execute_by(catcher_client)
        )
    finally:
        logging.info('Disconnected')
        await asyncio.gather(
            proxy_client.disconnect(),
            catcher_client.disconnect()
        )

if __name__ == '__main__':
    asyncio.run(run(
        load_config('configuration.json')
    ))