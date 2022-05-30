"""This module provides the RP To-Do config functionality."""

# import configparser
from functools import cache
from pathlib import Path

import typer

from . import TodoInitError, __app_name__
from . import logger

DEFAULT_DB_FILE_PATH = Path.home() / '.todo-cli-tddschn.db'
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
# CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.yaml"

# escape % in ini
# DEFAULT_DUE_DATE_FORMAT = '%%Y-%%m-%%d %%H:%%M:%%S'
DEFAULT_DUE_DATE_FORMAT = '%%m-%%d'
# DEFAULT_DATE_ADDED_FORMAT = '%%Y-%%m-%%d'
DEFAULT_DATE_ADDED_FORMAT = '%%m-%%d'
DEFAULT_FORMAT_DICT = {
    'due_date': DEFAULT_DUE_DATE_FORMAT,
    'date_added': DEFAULT_DATE_ADDED_FORMAT,
}

app = typer.Typer(name='config')


def create_config_dict() -> dict:
    """create a default config dict"""
    d = {
        'database': str(DEFAULT_DB_FILE_PATH),
        'format': {
            'due_date': DEFAULT_DUE_DATE_FORMAT,
            'date_added': DEFAULT_DATE_ADDED_FORMAT,
        },
        'hide': [],
    }
    return d


def init_app(db_path: Path, config_file_path: Path = CONFIG_FILE_PATH):
    """Initialize the application.
    get the config file,
    and add db_path to the config file"""
    import yaml

    config_dict = create_config_dict()
    config_s = yaml.safe_dump(config_dict)
    try:
        touch_config_file(config_file_path)
        config_file_path.write_text(config_s)
        typer.secho(f"Config file created at {config_file_path}", fg=typer.colors.GREEN)
    except:
        typer.secho(
            f'Creating config file {config_file_path} failed', fg=typer.colors.RED
        )
        raise typer.Exit(1)


def touch_config_file(config_file_path):
    config_file_path.parent.mkdir(exist_ok=True)
    config_file_path.touch(exist_ok=True)


def read_config(config_file: Path) -> dict:
    """read the config file to get the config dict"""
    import yaml

    logger.info(f"Reading config file: {config_file}")
    config_dict = yaml.safe_load(config_file.read_text())
    return config_dict


def get_database_path(config_file: Path) -> Path:
    """Read and returns the current path to the to-do database
    from the config file."""
    return Path(read_config(config_file)["database"])


@cache
def get_format(config_file: Path) -> dict[str, str]:
    """Get format specs from the config file."""
    try:
        format_dict = read_config(config_file)["format"]
        default_format_dict_copy = DEFAULT_FORMAT_DICT.copy()
        default_format_dict_copy.update(format_dict)
        return default_format_dict_copy
    except:
        return DEFAULT_FORMAT_DICT


@cache
def get_hide(config_file: Path) -> list[str]:
    """Get hide specs from the config file."""
    try:
        hide_l = read_config(config_file)["hide"]
        return list(map(str.lower, hide_l))
    except:
        return []


@app.command('path')
def get_config_path() -> str:
    """Get the path to the config file."""
    config_path: str = str(CONFIG_FILE_PATH)
    typer.secho(config_path)
    return config_path


@app.command('edit')
def edit_config() -> None:
    """Edit the config file."""
    touch_config_file(CONFIG_FILE_PATH)
    typer.echo(f"Opening the config file at {CONFIG_FILE_PATH}")
    typer.launch(f"{CONFIG_FILE_PATH}")


@app.command('db-path')
def get_db_path():
    """Get the path to the to-do database."""
    p = get_database_path(CONFIG_FILE_PATH)
    typer.secho(str(p))


@app.callback()
def main():
    """Getting and managing the config"""


if __name__ == '__main__':
    app()
