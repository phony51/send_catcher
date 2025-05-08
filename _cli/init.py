import click

from _cli.utils import ROOT_DIR
from config.app import AppConfig


@click.command(name='init', help='Init enviroment')
def init():
    abs_logs_dir = ROOT_DIR / AppConfig.LOGS_DIR
    abs_sessions_dir = ROOT_DIR / AppConfig.SESSIONS_DIR
    abs_config_path = ROOT_DIR / AppConfig.CONFIG_PATH
    abs_env_path = ROOT_DIR / '.env'
    abs_logs_dir.mkdir(exist_ok=True)
    abs_sessions_dir.mkdir(exist_ok=True)
    abs_env_path.touch()
    if not abs_config_path.exists():
        AppConfig().save_config()