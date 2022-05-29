import typer
from datetime import datetime
from pathlib import Path
from . import __app_name__, __version__, config, Status, Priority
from . import logger, _DEBUG
from .config import DEFAULT_DB_FILE_PATH, get_database_path
from sqlmodel import Session, delete, func
from .database import create_db_and_tables, engine, get_project_with_name
from .models import Project, Todo, ProjectCreate, ProjectRead, TodoCreate, TodoRead
from .utils import merge_desc, serialize_tags, deserialize_tags, todo_to_dict_with_project_name
from tabulate import tabulate

app = typer.Typer(name='info')


# @app.command(name="list")
# @app.command(name="ls")
@app.callback(invoke_without_command=False)
def info() -> None:
    """Get infos about todos"""


@app.command()
def count():
    """Get count of todos"""
    with Session(engine) as session:
        count = session.exec(func.count(Todo.id)).one()[0]  # type: ignore
        typer.secho(f"Total todos: {count}")