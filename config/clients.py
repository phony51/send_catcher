from config.base import CamelCaseBaseModel
from config.logger import LoggerConfig


class ClientConfig(CamelCaseBaseModel):
    api_id: int
    api_hash: str
    session_name: str
    phone: str


class ClientsConfig(CamelCaseBaseModel):
    catcher_client: ClientConfig
    proxy_client: ClientConfig
