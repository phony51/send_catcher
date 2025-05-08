import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.app import AppConfig
from config.logger import LoggerConfig


def setup_logger(logger_config: LoggerConfig):
    recorder = RotatingFileHandler(
        filename=Path(AppConfig.LOGS_DIR, logger_config.filename),
        maxBytes=logger_config.max_size_kb*1024,
        backupCount=logger_config.max_bak,
        encoding='utf-8'
    )
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
        level=logger_config.mapped_level,
        handlers=[recorder]
    )
