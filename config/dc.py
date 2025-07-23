from config.base import CamelCaseBaseModel


class DC(CamelCaseBaseModel):
    id: int
    ip: str
    port: int = 443

