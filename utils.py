from config.clients import ClientConfig
from core.clients_pool import ClientsPool


async def get_clients_pool(proxy_client_configs: list[ClientConfig]):
    for proxy_client_config in proxy_client_configs:
        if not await proxy_client_config.is_authorized():
            raise ValueError(f'Proxy client {proxy_client_config.api_id} is not authorized')
    return ClientsPool([proxy_client_config.client for proxy_client_config in proxy_client_configs])
            