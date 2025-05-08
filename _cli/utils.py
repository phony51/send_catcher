from functools import wraps
from pathlib import Path
from typing import Any, Callable
import click
from dotenv import find_dotenv
from config.app import AppConfig
from config.clients import ClientConfig


def fill_client_config(session_filename: str):
    return ClientConfig(
        api_id=click.prompt("Enter API ID", type=int),
        api_hash=click.prompt("Enter API Hash", ),
        phone=click.prompt("Enter phone number"),
        session_path=Path(AppConfig.SESSIONS_DIR, session_filename)
    )


async def create_session(client_config: ClientConfig):
    def enter_code():
        return click.prompt(f'Enter confirmation code ({client_config.phone})', type=int)
    async with await client_config.client.start(phone=client_config.phone, code_callback=enter_code):
        pass
        
        
def get_filter_client_func(phone: str):
    def func(client: ClientConfig):
        return client.phone == phone
    return func


def config_require(func: Callable[[Any], AppConfig]):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs, app_config=AppConfig.load_config()).save_config()
        except Exception as e:
            raise e
    return inner


ROOT_DIR = Path(find_dotenv()).parent
