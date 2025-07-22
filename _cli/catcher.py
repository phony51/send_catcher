import click

from _cli.utils import ROOT_DIR, config_require, fill_client_config
from config.app import AppConfig

catcher_group = click.Group(name='catcher', help='Operate catcher client')


@catcher_group.command('add')
@click.option('--hard', is_flag=True, show_default=False, help='Overwrite current client')
@config_require
def catcher_add(hard: bool, app_config: AppConfig):
    app_config.clients.add_catcher_client(
        fill_client_config(app_config.clients.CATCHER_SESSION_FILENAME),
        hard
    )
    return app_config


@catcher_group.command('remove')
@config_require
def catcher_remove(app_config: AppConfig):
    app_config.clients.remove_catcher_client(ROOT_DIR)
    return app_config
