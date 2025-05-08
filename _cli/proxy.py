import click

from _cli.utils import ROOT_DIR, config_require, fill_client_config, get_filter_client_func
from config.app import AppConfig


proxy_group = click.Group(name='proxy', help='Operate proxy clients')
@proxy_group.command('add')
@config_require
def proxy_add(app_config: AppConfig):
    app_config.clients.add_proxy_client(fill_client_config(app_config.clients.next_proxy_session_filename))    
    return app_config

@proxy_group.command('remove')
@click.argument('phones', nargs=-1, required=True)
@config_require
def proxy_remove(phones: list[str], app_config: AppConfig):
    for phone in phones:
        if app_config.clients.remove_proxy_client(ROOT_DIR, get_filter_client_func(phone)):
            click.echo(phone)
    return app_config
    
        