import typer
from datetime import datetime
from pathlib import Path
from . import __app_name__, __version__, config, Status, Priority
from . import logger, _DEBUG
from .config import DEFAULT_DB_FILE_PATH, get_database_path
from sqlmodel import Session, delete, case, nullslast, select, col
from .database import create_db_and_tables, engine, get_project_with_name
from .models import Project, Todo, ProjectCreate, ProjectRead, TodoCreate, TodoRead
from .utils import (
    merge_desc,
    serialize_tags,
    deserialize_tags,
    todo_to_dict_with_project_name,
    format_datetime,
)
from tabulate import tabulate

app = typer.Typer(name='ls')


def _list_todos(
    todos: list[Todo], filtered: bool = False, date_added_full: bool = False
) -> None:
    todo_list = [todo_to_dict_with_project_name(x, date_added_full) for x in todos]
    if filtered:
        no_todo_found_message = "No matching to-do found."
    else:
        no_todo_found_message = "There are no tasks in the to-do list yet"
    if len(todo_list) == 0:
        typer.secho(no_todo_found_message, fg=typer.colors.RED, err=True)
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    table = tabulate(todo_list, headers='keys')
    typer.secho(table)


@app.callback(invoke_without_command=True)
def order_by_priority_then_due_date(
    description: str = typer.Option(
        None,
        "--description",
        "-d",
    ),
    priority: Priority = typer.Option(None, "--priority", "-p", case_sensitive=False),
    status: Status = typer.Option(None, "--status", "-s", case_sensitive=False),
    project: str = typer.Option(
        None,
        "--project",
        "-pr",
    ),
    tags: str = typer.Option(
        None,
        "--tags",
        "-t",
    ),
    due_date: datetime = typer.Option(
        None,
        "--due-date",
        "-dd",
    ),
    due_date_before: datetime = typer.Option(
        None,
        "--due-date-before",
        "-ddb",
    ),
    due_date_after: datetime = typer.Option(
        None,
        "--due-date-after",
        "-dda",
    ),
    date_added_before: datetime = typer.Option(
        None,
        "--date-added-before",
        "-dab",
    ),
    date_added_after: datetime = typer.Option(
        None,
        "--date-added-after",
        "-daa",
    ),
    full_date_added: bool = typer.Option(
        False, "--full-date-added", "-fda", help='Include time in the date_added column'
    ),
):
    """list all to-dos, ordered by priority and due date."""
    whens = {'low': 0, 'medium': 1, 'high': 2}
    wheres = []
    if description is not None:
        wheres.append(col(Todo.description).like(f'%{description}%'))
    if priority is not None:
        wheres.append(col(Todo.priority) == priority)
    if status is not None:
        wheres.append(col(Todo.status) == status)
    if project is not None:
        wheres.append(col(Todo.project_id) == get_project_with_name(project).id)
    if tags is not None:
        wheres.append(col(Todo.tags).like(f'%{tags}%'))
    if due_date is not None:
        wheres.append(col(Todo.due_date) == due_date)
    if due_date_before is not None:
        wheres.append(col(Todo.due_date) < due_date_before)
    if due_date_after is not None:
        wheres.append(col(Todo.due_date) > due_date_after)
    if date_added_before is not None:
        wheres.append(col(Todo.date_added) < date_added_before)
    if date_added_after is not None:
        wheres.append(col(Todo.date_added) > date_added_after)
    sort_logic = case(value=Todo.priority, whens=whens)
    with Session(engine) as session:
        todos = (
            session.query(Todo)
            .where(*wheres)
            .order_by(sort_logic.desc(), nullslast(Todo.due_date))
            .all()
        )
    _list_todos(todos, filtered=bool(wheres), date_added_full=full_date_added)


@app.command('tag')
def filter_by_tags(tag: str):
    """Filter to-dos by tag."""
    with Session(engine) as session:
        todos = session.exec(select(Todo).where(col(Todo.tags).like(f"%{tag}%"))).all()
    _list_todos(todos, True)


@app.command('project')
def filter_by_project(project_name: str):
    """Filter to-dos by project."""
    with Session(engine) as session:
        todos = session.exec(
            select(Todo).where(
                col(Todo.project_id) == get_project_with_name(project_name).id
            )
        ).all()
    _list_todos(todos, True)
