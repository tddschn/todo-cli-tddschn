"""This module provides the RP To-Do config functionality."""

import configparser
from pathlib import Path

import typer

from . import DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__

DEFAULT_DB_FILE_PATH = Path.home() / '.todo-cli-tddschn.db'
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_app(db_path: Path) -> int:
    """Initialize the application.
    get the config file,
    and add db_path to the config file"""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    create_db = _create_database(db_path)
    return create_db


def _init_config_file() -> int:
    """touch the config file."""
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS


def _create_database(db_path: Path) -> int:
    """write db_path to config file."""
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": str(db_path)}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS


def get_database_path(config_file: Path) -> Path:
    """Read and returns the current path to the to-do database
	from the config file."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])