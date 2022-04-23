#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import typer
from . import __app_name__, __version__, config, Status, Priority
from . import logger, _DEBUG
from .config import DEFAULT_DB_FILE_PATH, get_database_path
from sqlmodel import Session, delete
from .database import create_db_and_tables, engine, get_project_with_name
from .models import Project, Todo, ProjectCreate, ProjectRead, TodoCreate, TodoRead
from .utils import merge_desc, serialize_tags, deserialize_tags, todo_to_dict_with_project_name
from tabulate import tabulate

# logger = None
# _DEBUG = None

app = typer.Typer(name='todo')
app.add_typer(config.app, name='config')


def _check_db_exists() -> None:
    db_path = get_database_path(config.CONFIG_FILE_PATH)
    if not db_path.exists() or db_path.stat().st_size == 0:
        typer.secho(
            f'Database not initialized. Run `todo init` to initialize.',
            fg=typer.colors.RED,
            err=True)
        raise typer.Abort()


# _check_db_inited()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


# def _verbose_callback(value: bool) -> None:
#     global logger
#     global _DEBUG
#     logger, _DEBUG = get_logger(do_log=value)

init_db_path_opt = typer.Option(
    DEFAULT_DB_FILE_PATH,
    "--db-path",
    "-db",
    prompt="to-do database location?",
)


@app.command()
def init(db_path: Path = init_db_path_opt,
         config_file_path: Path = config.CONFIG_FILE_PATH) -> None:
    """Initialize the to-do database."""
    config.init_app(db_path, config_file_path)
    try:
        create_db_and_tables()
        typer.secho('Database created successfully',
                    fg=typer.colors.GREEN,
                    err=True)
    except Exception as e:
        typer.secho(f'Creating database failed with "{e}"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)


@app.command()
def re_init(
    db_path: Path = init_db_path_opt,
    config_file_path: Path = config.CONFIG_FILE_PATH,
    force: bool = typer.Option(False,
                               "--force",
                               "-f",
                               help="Force re-initialization"),
) -> None:
    """Re-initialize the to-do database.
    This will delete the current database and create a new one."""

    def _re_init(db_path: Path, config_file_path):
        # delete the old database
        old_db_path = get_database_path(config.CONFIG_FILE_PATH)
        old_db_path.unlink(missing_ok=True)

        # initialize the new database
        init(db_path=db_path, config_file_path=config_file_path)

    if force:
        _re_init(db_path, config_file_path)
    else:
        typer.confirm(
            "Are you sure you want to re-initialize the to-do database?",
            abort=True)
        _re_init(db_path, config_file_path)


@app.command('a')
# @app.command()
def add(
        description: list[str] = typer.Argument(...),
        priority: Priority = typer.Option(Priority.MEDIUM,
                                          "--priority",
                                          "-p",
                                          case_sensitive=False),
        status: Status = typer.Option(Status.TODO,
                                      "--status",
                                      "-s",
                                      case_sensitive=False),
        project: str = typer.Option(
            None,
            "--project",
            "-pr",
        ),
        tags: list[str] = typer.Option(
            None,
            "--tags",
            "-t",
        ),
        due_date: datetime = typer.Option(
            None,
            "--due-date",
            "-dd",
        ),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    todo_create = TodoCreate(
        description=merge_desc(description),
        priority=priority,
        status=status,
        tags=serialize_tags(tags),
        due_date=due_date,
        project_id=get_project_with_name(project).id if project else None,
    )
    with Session(engine) as session:
        db_todo = Todo.from_orm(todo_create)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        typer.secho(f'Added to-do # {db_todo.id}: "{db_todo.description}"',
                    fg=typer.colors.GREEN,
                    err=True)


# @app.command(name="list")
@app.command(name="ls")
def list_all() -> None:
    """list all to-dos."""
    # _check_db_inited() # not working
    with Session(engine) as session:
        todos = session.query(Todo).all()
        todo_list = [todo_to_dict_with_project_name(x) for x in todos]
    if len(todo_list) == 0:
        typer.secho("There are no tasks in the to-do list yet",
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    table = tabulate(todo_list, headers='keys')
    typer.secho(table)


# @app.command(name="complete")
# @app.command(name="comp")
# def


@app.command(name='g')
# @app.command(name='get')
def get_todo(todo_id: int) -> None:
    """Get a to-do by ID."""
    with Session(engine) as session:
        _get_todo(todo_id, session, True)


def _get_todo(todo_id, session, output: bool = False) -> Todo:
    todo = session.get(Todo, todo_id)
    if todo is None:
        typer.secho(f'No to-do with id {todo_id}',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit()
    if output:
        todo_list = [todo_to_dict_with_project_name(todo)]
        table = tabulate(todo_list, headers='keys')
        typer.secho(table)
    return todo


# @app.command(name='s')
# @app.command(name='set')
# def set_status(todo_id: int, status: Status = Status.DONE) -> None:
#     """Set a todo's status using its TODO_ID."""
#     modify(todo_id, status=status)


@app.command(name='m')
# @app.command(name='modify')
def modify(
        # ctx: typer.Context,
        todo_id: int = typer.Argument(...),
        description: str = typer.Option(
            None,
            "--description",
            "-d",
        ),
        priority: Priority = typer.Option(None,
                                          "--priority",
                                          "-p",
                                          case_sensitive=False),
        status: Status = typer.Option(None,
                                      "--status",
                                      "-s",
                                      case_sensitive=False),
        project: str = typer.Option(
            None,
            "--project",
            "-pr",
        ),
        tags: list[str] = typer.Option(
            None,
            "--tags",
            "-t",
        ),
        due_date: datetime = typer.Option(
            None,
            "--due-date",
            "-dd",
        ),
) -> None:
    """Modify a to-do by setting it as done using its TODO_ID."""
    # print(ctx.args)
    # https://click.palletsprojects.com/en/7.x/api/#context

    with Session(engine) as session:
        todo = _get_todo(todo_id, session)
        todo.description = description if description is not None else todo.description
        todo.priority = priority if priority is not None else todo.priority
        todo.status = status if status is not None else todo.status
        todo.project_id = get_project_with_name(
            project).id if project is not None else todo.project_id
        todo.tags = serialize_tags(tags) if tags is not None else todo.tags
        todo.due_date = due_date if due_date is not None else todo.due_date
        session.add(todo)
        session.commit()
        typer.secho(f'Modified todo # {todo_id}:',
                    fg=typer.colors.GREEN,
                    err=True)
        _get_todo(todo_id, session, True)


@app.command('rm')
# @app.command()
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove a to-do using its TODO_ID."""
    with Session(engine) as session:
        todo = _get_todo(todo_id, session)
        if not force:
            typer.confirm(f'Are you sure you want to delete todo # {todo_id}?',
                          abort=True)
        session.delete(todo)
        session.commit()
        typer.secho(f'Removed todo # {todo_id}',
                    fg=typer.colors.GREEN,
                    err=True)


@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all to-dos?",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove all to-dos."""
    with Session(engine) as session:
        if not force:
            typer.confirm(f'Are you sure you want to delete all to-dos?',
                          abort=True)
        statement = delete(Todo)
        result = session.exec(statement)  # type: ignore
        session.commit()
        typer.secho(f'Removed {result.rowcount} to-dos',
                    fg=typer.colors.GREEN,
                    err=True)


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    # verbose: bool = typer.Option(False,
    #                              help='Show verbose output.',
    #                              callback=_verbose_callback),
) -> None:
    """
    tddschn's command line todo app
    """
    # print(ctx.invoked_subcommand)
    # raise typer.Abort()
    if ctx.invoked_subcommand not in ['init', 're-init']:
        _check_db_exists()


if __name__ == '__main__':
    app()
