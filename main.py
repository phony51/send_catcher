import asyncio
import logging
import re
from config.app import AppConfig
from logger.logger import setup_logger
from utils import get_clients, load_config


async def run(app_config: AppConfig):
    setup_logger(app_config.logger)
    
    try:
        await proxy_client.start()
        await .start()
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
        load_config()
    ))
