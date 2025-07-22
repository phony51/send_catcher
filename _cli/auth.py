import asyncio
import click
from _cli.utils import config_require, create_session
from config.app import AppConfig


async def _auth_all(app_config: AppConfig):
    await create_session(app_config.clients.catcher)
    await create_session(app_config.clients.proxy)


@click.command(name='auth', help='Authorize clients')
@config_require
def auth(app_config: AppConfig):
    asyncio.new_event_loop().run_until_complete(_auth_all(app_config))
    return app_config
