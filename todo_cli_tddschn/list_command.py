import typer
from datetime import datetime
from pathlib import Path
from . import __app_name__, __version__, config, Status, Priority
from . import logger, _DEBUG
from .config import DEFAULT_DB_FILE_PATH, get_database_path
from sqlmodel import Session, delete, case, nullslast
from .database import create_db_and_tables, engine, get_project_with_name
from .models import Project, Todo, ProjectCreate, ProjectRead, TodoCreate, TodoRead
from .utils import merge_desc, serialize_tags, deserialize_tags, todo_to_dict_with_project_name
from tabulate import tabulate

app = typer.Typer(name='ls')


# @app.command(name="list")
# @app.command(name="ls")
def list_all() -> None:
    """list all to-dos."""
    # _check_db_inited() # not working
    with Session(engine) as session:
        todos = session.query(Todo).all()
    _list_todos(todos)


def _list_todos(todos: list[Todo]):
    todo_list = [todo_to_dict_with_project_name(x) for x in todos]
    if len(todo_list) == 0:
        typer.secho("There are no tasks in the to-do list yet",
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    table = tabulate(todo_list, headers='keys')
    typer.secho(table)


@app.callback(invoke_without_command=True)
def order_by_priority_then_due_date():
    whens = {'low': 0, 'medium': 1, 'high': 2}
    sort_logic = case(value=Todo.priority, whens=whens).label("priority")
    with Session(engine) as session:
        todos = session.query(Todo).order_by(sort_logic.desc(),
                                             nullslast(Todo.due_date)).all()
    _list_todos(todos)
