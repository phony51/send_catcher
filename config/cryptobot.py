from config.base import CamelCaseBaseModel


class CryptoBotConfig(CamelCaseBaseModel):
    domain: str
    id: int