import logging
from pathlib import Path
from typing import ClassVar, Optional
from config.base import CamelCaseBaseModel
from config.clients import ClientsConfig
from config.cryptobot import CryptoBotConfig
from config.logger import LoggerConfig


class AppConfig(CamelCaseBaseModel):
    CONFIG_PATH: ClassVar[str] = 'configuration.lock.json'
    SESSIONS_DIR: ClassVar[str] = 'sessions'
    LOGS_DIR: ClassVar[str] = 'logs'

    clients: ClientsConfig = ClientsConfig()
    cryptobot: CryptoBotConfig = CryptoBotConfig()
    logger: LoggerConfig = LoggerConfig()

    def init_enviroment(self):
        Path(self.SESSIONS_DIR).mkdir(exist_ok=True)
        Path(self.LOGS_DIR).mkdir(exist_ok=True)

    @classmethod
    def load_config(cls):
        if Path(cls.CONFIG_PATH).exists():
            with open(cls.CONFIG_PATH, 'r') as configuration:
                return cls.model_validate_json(configuration.read())
        cls.__init__(cls())
        return cls.model_copy(cls())

    def save_config(self):
        with open(self.CONFIG_PATH, 'w') as configuration:
            configuration.write(self.model_dump_json(indent=4))
