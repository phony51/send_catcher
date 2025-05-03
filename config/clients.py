from config.base import CamelCaseBaseModel
from config.logger import LoggerConfig


class ClientConfig(CamelCaseBaseModel):
    api_id: int
    api_hash: str
    phone: str


class ClientsConfig(CamelCaseBaseModel):
    catcher: ClientConfig
    proxy: ClientConfig
