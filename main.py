import asyncio
import logging

from config.app import AppConfig
from core.catcher import CatcherLoop, ChequeProcessor
from logger.logger import setup_logger


async def run(app_config: AppConfig):
    setup_logger(app_config.logger)

    if not await app_config.clients.catcher.is_authorized():
        raise ValueError('Catcher client is not authorized')

    proxy_client = app_config.clients.proxy.client
    await proxy_client.start()
    cryptobot = await proxy_client.get_entity("send")
    cheque_processor = ChequeProcessor(
        domain=app_config.cryptobot.domain,
        cryptobot=cryptobot,
        client=app_config.clients.proxy.client
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
