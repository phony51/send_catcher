from config.base import CamelCaseBaseModel
from config.clients import Clients

CONFIG_PATH = 'configuration.json'
CRYPTOBOT_USERNAME = 'CryptoBot'


class AppConfig(CamelCaseBaseModel):
    clients: Clients
