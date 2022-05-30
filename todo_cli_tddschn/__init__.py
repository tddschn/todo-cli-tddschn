__version__ = '2.0.0'
__app_name__ = 'todo'
__app_name_full__ = 'todo-cli-tddschn'

from dataclasses import dataclass
from enum import Enum
from typing import Any

try:
    from logging_utils_tddschn import get_logger
    logger, _DEBUG = get_logger(__app_name__)
except:
    import logging
    from logging import NullHandler
    logger = logging.getLogger(__app_name__)
    logger.addHandler(NullHandler())


class Priority(str, Enum):
    """Priority levels for to-dos."""

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Status(str, Enum):
    """Status of a to-do."""
    TODO = 'todo'
    DONE = 'done'
    DELETED = 'deleted'
    CANCELLED = 'cancelled'
    WIP = 'wip'


# create a custom exception class TodoInitError
class TodoInitError(Exception):
    """Custom exception class for todo-cli-tddschn."""

    def __init__(self, message: str, error_code: int = 1) -> None:
        """Initialize the TodoInitError class."""
        super().__init__(message)
        self.error_code = error_code
