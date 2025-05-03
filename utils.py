from pathlib import Path
from telethon import TelegramClient
from config.clients import ClientConfig
from pathlib import Path
from config.app import AppConfig


def get_clients(proxy_client_config: ClientConfig, catcher_client_config: ClientConfig) -> tuple[TelegramClient, TelegramClient]:
    return TelegramClient(
        session=Path('sessions', 'proxy'),
        api_id=proxy_client_config.api_id,
        api_hash=proxy_client_config.api_hash
    ), \
        TelegramClient(
        session=Path('sessions', 'catcher'),
        api_id=catcher_client_config.api_id,
        api_hash=catcher_client_config.api_hash
    )


def load_config(path: Path = 'configuration.json'):
    with open(path, 'r') as configuration:
        app_config = AppConfig.model_validate_json(configuration.read())
    return app_config
