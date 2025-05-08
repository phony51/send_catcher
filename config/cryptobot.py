from config.base import CamelCaseBaseModel


class CryptoBotConfig(CamelCaseBaseModel):
    domain: str = 'send'
    id: int = 1559501630