import asyncio
import logging

from telethon import events

from config.app import AppConfig, CRYPTOBOT_USERNAME, CONFIG_PATH
from core.catcher import Catcher, Cryptobot


async def run(app_config: AppConfig):
    catcher_config = app_config.clients.catcher
    await catcher_config.client.start(
        catcher_config.phone,
        catcher_config.password
    )
    proxy_config = app_config.clients.proxy
    proxy_client = proxy_config.client
    await proxy_client.start(
        proxy_config.phone,
        proxy_config.password
    )

    await proxy_client.start()
    cryptobot = Cryptobot(
        ent=await proxy_client.get_entity(CRYPTOBOT_USERNAME),
        client=proxy_client
    )
    logging.info('Authorization successfully')

    try:
        await Catcher(app_config.clients.catcher.client, cryptobot).run()
    finally:
        logging.info('Disconnected')


if __name__ == '__main__':
    with open(CONFIG_PATH, 'r') as f:
        config = f.read()
    asyncio.run(run(
        AppConfig.model_validate_json(config)
    ))
