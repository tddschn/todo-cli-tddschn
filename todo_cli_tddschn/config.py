"""This module provides the RP To-Do config functionality."""

import configparser
from pathlib import Path

import typer

from . import TodoInitError, __app_name__
from . import logger

DEFAULT_DB_FILE_PATH = Path.home() / '.todo-cli-tddschn.db'
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

# DEFAULT_DUE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DUE_DATE_FORMAT = '%m-%d'
# DEFAULT_DATE_ADDED_FORMAT = '%Y-%m-%d'
DEFAULT_DATE_ADDED_FORMAT = '%m-%d'
DEFAULT_FORMAT_SPEC = {
    'due_date': DEFAULT_DUE_DATE_FORMAT,
    'date_added': DEFAULT_DATE_ADDED_FORMAT,
}

app = typer.Typer(name='config')


def create_default_config_object() -> configparser.ConfigParser:
    """Create a default config object."""
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": str(DEFAULT_DB_FILE_PATH)}
    config_parser["Format"] = DEFAULT_FORMAT_SPEC
    return config_parser


def init_app(db_path: Path, config_file_path: Path = CONFIG_FILE_PATH):
    """Initialize the application.
    get the config file,
    and add db_path to the config file"""
    config_parser = create_default_config_object()
    try:
        config_file_path.parent.mkdir(exist_ok=True)
        config_file_path.touch(exist_ok=True)
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
        typer.secho(f"Config file created at {config_file_path}", fg=typer.colors.GREEN)
    except:
        # raise TodoInitError(f'Creating config file {config_file_path} failed')
        typer.secho(
            f'Creating config file {config_file_path} failed', fg=typer.colors.RED
        )
        raise typer.Exit(1)


def read_config(config_file: Path) -> configparser.ConfigParser:
    logger.info(f"Reading database path from {config_file}")
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return config_parser


def get_database_path(config_file: Path) -> Path:
    """Read and returns the current path to the to-do database
    from the config file."""
    config_parser = read_config(config_file)
    return Path(config_parser["General"]["database"])


def get_format(config_file: Path) -> configparser.SectionProxy | dict[str, str]:
    """Get format specs from the config file."""
    config_parser = read_config(config_file)
    try:
        format_specs = config_parser["Format"]
    except:
        format_specs = DEFAULT_FORMAT_SPEC
    return format_specs


@app.command('path')
def get_config_path() -> str:
    """Get the path to the config file."""
    config_path: str = str(CONFIG_FILE_PATH)
    typer.secho(config_path)
    return config_path


@app.command('edit')
def edit_config() -> None:
    """Edit the config file."""
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
