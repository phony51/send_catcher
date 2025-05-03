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