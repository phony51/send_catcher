import logging
from logging.handlers import RotatingFileHandler

from config.logger import LoggerConfig


def setup_logger(logger_config: LoggerConfig):
    recorder = RotatingFileHandler(
        filename=logger_config.path,
        maxBytes=logger_config.max_size_kb*1024,
        backupCount=logger_config.max_bak,
        encoding='utf-8'
    )
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
        level=logger_config.mapped_level,
        handlers=[recorder]
    )
