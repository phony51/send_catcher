import click

from _cli.utils import ROOT_DIR, config_require, fill_client_config
from config.app import AppConfig

proxy_group = click.Group(name='proxy', help='Operate proxy client')


@proxy_group.command('add')
@click.option('--hard', is_flag=True, show_default=False, help='Overwrite current client')
@config_require
def proxy_add(hard: bool, app_config: AppConfig):
    app_config.clients.add_proxy_client(
        fill_client_config(app_config.clients.PROXY_SESSION_FILENAME),
        hard
    )
    return app_config


@proxy_group.command('remove')
@config_require
def proxy_remove(app_config: AppConfig):
    app_config.clients.remove_proxy_client(ROOT_DIR)
    return app_config
