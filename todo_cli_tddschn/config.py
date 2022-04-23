"""This module provides the RP To-Do config functionality."""

import configparser
from pathlib import Path

import typer

from . import TodoInitError, __app_name__
from . import logger

DEFAULT_DB_FILE_PATH = Path.home() / '.todo-cli-tddschn.db'
CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

app = typer.Typer(name='config')


def init_app(db_path: Path, config_file_path: Path = CONFIG_FILE_PATH):
    """Initialize the application.
    get the config file,
    and add db_path to the config file"""
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": str(db_path)}
    try:
        config_file_path.parent.mkdir(exist_ok=True)
        config_file_path.touch(exist_ok=True)
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
        typer.secho(f"Config file created at {config_file_path}",
                    fg=typer.colors.GREEN)
    except:
        # raise TodoInitError(f'Creating config file {config_file_path} failed')
        typer.secho(f'Creating config file {config_file_path} failed',
                    fg=typer.colors.RED)
        raise typer.Exit(1)


def get_database_path(config_file: Path) -> Path:
    """Read and returns the current path to the to-do database
    from the config file."""
    logger.info(f"Reading database path from {config_file}")
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


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
