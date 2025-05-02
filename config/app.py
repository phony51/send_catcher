import logging
from pathlib import Path
from config.base import CamelCaseBaseModel
from config.clients import ClientsConfig
from config.cryptobot import CryptoBotConfig
from config.logger import LoggerConfig


class AppConfig(CamelCaseBaseModel):
    clients: ClientsConfig
    crypto_bot: CryptoBotConfig
    logger: LoggerConfig


def load_config(path: Path):
    with open(path, 'r') as configuration:
        app_config = AppConfig.model_validate_json(configuration.read())
    logging.getLogger(__name__).info('Configuration loaded')
    return app_config
