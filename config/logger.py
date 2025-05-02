from enum import StrEnum
from pathlib import Path
import logging
from config.base import CamelCaseBaseModel


class LogLevel(StrEnum):
    DEBUG = 'debug'
    INFO = 'info'
    FATAL = 'fatal'


log_level_mapping = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.FATAL: logging.FATAL
}


class LoggerConfig(CamelCaseBaseModel):
    level: LogLevel
    max_bak: int
    max_size_kb: int
    path: Path

    @property
    def mapped_level(self):
        return log_level_mapping[self.level]
