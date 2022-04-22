#!/usr/bin/env python3

from pathlib import Path
import typer
from . import __app_name__, __version__, config, ERRORS
from .config import DEFAULT_DB_FILE_PATH
from .database import create_db_and_tables, engine
from .models import Project, Todo

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def init(
    db_path: Path = typer.Option(
        DEFAULT_DB_FILE_PATH,
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
            err=True)
        raise typer.Exit(1)
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
    db_path: Path = typer.Option(
        DEFAULT_DB_FILE_PATH,
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
    force: bool = typer.Option(False,
                               "--force",
                               "-f",
                               help="Force re-initialization"),
) -> None:
    """Re-initialize the to-do database."""

    def _re_init(db_path: Path):
        # delete the old database
        old_db_path = get_database_path(config.CONFIG_FILE_PATH)
        old_db_path.unlink(missing_ok=True)

        # initialize the new database
        init(db_path=db_path)

    if force:
        _re_init(db_path)
    else:
        typer.confirm(
            "Are you sure you want to re-initialize the to-do database?",
            abort=True)
        _re_init(db_path)


def get_todoer() -> Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho('Config file not found. Please, run "todo init"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)
    if db_path.exists():
        return Todoer(db_path)
    else:
        typer.secho('Database not found. Please, run "todo init"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)


@app.command('a')
@app.command()
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
    todoer = get_todoer()
    curr_todo = todoer.add(description, priority, status, project, tags,
                           due_date)
    error = curr_todo.error
    todo = curr_todo.todo
    if error:
        typer.secho(f'Adding to-do failed with "{ERRORS[error]}"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo.description}" was added """  # type: ignore
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
            err=True)


@app.command(name="list")
@app.command(name="ls")
def list_all() -> None:
    """list all to-dos."""
    todoer = get_todoer()
    todo_item_list = todoer.get_todo_all()
    logger.info(f"todo_item_list: {todo_item_list}")
    todo_list = [row2dict(x) for x in todo_item_list]
    if len(todo_list) == 0:
        typer.secho("There are no tasks in the to-do list yet",
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    # tabulate(todo_list, headers=['id', 'description', 'priority', 'status', 'project', 'tags', 'due_date'])
    table = tabulate(todo_list, headers='keys')
    typer.secho(table)


# @app.command(name="complete")
# @app.command(name="comp")
# def


@app.command(name='g')
@app.command(name='get')
def get_todo(todo_id: int) -> None:
    """Get a to-do by ID."""
    todoer = get_todoer()
    todo = todoer.get_todo(todo_id)
    error = todo.error
    todo = todo.todo
    if error:
        typer.secho(f'Getting todo failed with "{ERRORS[error]}"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)
    else:
        todo_list = [row2dict(todo)]
        table = tabulate(todo_list, headers='keys')
        typer.secho(table)


@app.command(name='s')
@app.command(name='set')
def set_status(todo_id: int, status: Status = Status.DONE) -> None:
    """Set a todo's status using its TODO_ID."""
    modify(todo_id, status=status)


@app.command(name='m')
@app.command(name='modify')
def modify(
        todo_id: int = typer.Argument(...),
        desc: str = typer.Option(
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
    todoer = get_todoer()
    get = todoer.get_todo(todo_id)
    get_error = get.error
    if get_error:
        typer.secho(f'Getting todo failed with "{ERRORS[get_error]}"',
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)
    todo_orig = get.todo
    logger.info(f"todo_orig: {todo_orig}")
    # from icecream import ic
    # pri = todo_orig.priority # type: ignore
    # ic(pri, type(pri)) # type: ignore
    assert todo_orig is not None
    desc = desc if desc is not None else todo_orig.description
    priority = priority if priority is not None else todo_orig.priority
    status = status if status is not None else todo_orig.status
    project = project if project is not None else todo_orig.project
    tags = tags if tags is not None else deserialize_tags(todo_orig.tags)
    due_date_opt = due_date if due_date is not None else todo_orig.due_date

    modify = todoer.modify(todo_id, desc, priority, status, project, tags,
                           due_date_opt)
    todo = modify.todo
    error = modify.error
    if error:
        typer.secho(
            f'Modifying to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
            err=True)
        raise typer.Exit(1)
    else:
        assert todo is not None
        typer.secho(f"""to-do # {todo_id} modified!""",
                    fg=typer.colors.GREEN,
                    err=True)
        todo_list = [row2dict(todo)]
        table = tabulate(todo_list, headers='keys')
        typer.secho(table)


@app.command('rm')
@app.command()
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
    todoer = get_todoer()

    def _remove(todo: TodoItem):
        remove = todoer.remove(todo_id)
        logger.info(f"remove: {remove}")
        error = remove.error
        if error:
            typer.secho(
                f'Removing to-do # {todo_id}: {todo.description} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
                err=True)
            raise typer.Exit(1)
        else:
            typer.secho(f"""to-do # {todo_id}: {todo.description} removed!""",
                        fg=typer.colors.GREEN,
                        err=True)

    get = todoer.get_todo(todo_id)
    error = get.error
    todo = get.todo
    assert todo is not None
    if error:
        typer.secho(
            f'Getting to-do # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
            err=True)
        raise typer.Exit(1)

    if force:
        _remove(todo)
    else:
        assert todo is not None
        delete = typer.confirm(
            f"Delete to-do # {todo_id}: {todo.description}?", err=True)
        if delete:
            _remove(todo)
        else:
            typer.echo("Operation canceled")


@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all to-dos?",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove all to-dos."""
    todoer = get_todoer()
    if force:
        remove = todoer.remove_all()
        error = remove
        if error:
            typer.secho(
                f'Removing to-dos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho("All to-dos were removed", fg=typer.colors.GREEN)
    else:
        typer.echo("Operation canceled")


@app.callback()
def main(version: bool = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback,
    is_eager=True,
)) -> None:
    return


if __name__ == '__main__':
    app()
