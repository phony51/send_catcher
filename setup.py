import asyncio
from config.app import AppConfig
from core.executors.auth import AuthExecutor
from utils import get_clients, load_config


async def setup(config: AppConfig):
    proxy_client, catcher_client = get_clients(
        config.clients.proxy, config.clients.catcher)

    await AuthExecutor().execute_by(proxy_client, config.clients.proxy.phone)
    await AuthExecutor().execute_by(catcher_client, config.clients.catcher.phone)

if __name__ == "__main__":
    asyncio.run(setup(load_config()))
