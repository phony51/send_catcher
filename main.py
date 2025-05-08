import asyncio
import logging
import re
from config.app import AppConfig
from core.executors.catcher import CatcherLoop, ChequeProcessor
from logger.logger import setup_logger
from utils import get_clients_pool


async def run(app_config: AppConfig):
    setup_logger(app_config.logger)
    
    if not await app_config.clients.catcher.is_authorized():
        raise ValueError('Catcher client is not authorized')
    
    cheque_processor = ChequeProcessor(
        domain=app_config.cryptobot.domain,
        bot_id=app_config.cryptobot.id,
        clients_pool=await get_clients_pool(app_config.clients.proxy),
        cheque_id_regex=re.compile(r'CQ[A-Za-z0-9]{10}')
    )
    logging.debug('Authorization successfully')
    
    try:
        await CatcherLoop(app_config.clients.catcher.client, cheque_processor).run()
    finally:
        logging.info('Disconnected')

if __name__ == '__main__':
    asyncio.run(run(
        AppConfig.load_config()
    ))
