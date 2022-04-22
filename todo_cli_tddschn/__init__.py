__version__ = '0.2.1'
__app_name__ = 'todo'

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

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_CONNECTION_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    DB_DELETE_ERROR,
    DB_INSERT_ERROR,
    DB_UPDATE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(11)

ERRORS = {
    DIR_ERROR: 'config directory error',
    FILE_ERROR: 'config file error',
    DB_CONNECTION_ERROR: 'database connection error',
    DB_READ_ERROR: 'database read error',
    DB_WRITE_ERROR: 'database write error',
    ID_ERROR: 'to-do id error',
    DB_DELETE_ERROR: 'database delete error',
    DB_INSERT_ERROR: 'database insert error',
    DB_UPDATE_ERROR: 'database update error',
}


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


# @dataclass
# class TodoItem:
#     """Create a to-do item."""
#     id: int
#     description: str
#     priority: Priority
#     status: Status
#     project: str
#     tags: str
#     due_date: datetime | None


@dataclass
class DBResponse:
    # todo_list: list[TodoItem]
    error: int


@dataclass
class SessionResponse:
    session: Any
    error: int


@dataclass
class CurrentTodo:
    # todo: TodoItem | None
    error: int
