from configparser import SectionProxy
from datetime import datetime
import json
from sqlmodel import Session, select
from .database import engine
from .models import Project, Todo
import typer
from tabulate import tabulate
from . import __app_name__
from .config import CONFIG_FILE_PATH, get_format, get_hide


def merge_desc(desc_l: list[str]) -> str:
    return ' '.join(desc_l)


def format_datetime(
    d: datetime | None, full: bool = False, date_format: str | None = None
) -> str:
    if d is None:
        return ''
    if date_format is not None:
        return d.strftime(date_format)
    if full:
        return d.strftime('%Y-%m-%d %H:%M:%S')
    if d.year == datetime.now().year:
        return d.strftime('%m-%d')
    return d.strftime('%Y-%m-%d')


def serialize_tags(tags: list[str]) -> str:
    return json.dumps(tags)


def deserialize_tags(tags_s: str) -> list[str]:
    return json.loads(tags_s)


def str_self_or_empty(s) -> str:
    if s is None:
        return ''
    return str(s)


def todo_to_dict_with_project_name(
    todo: Todo,
    date_added_full_date: bool = False,
    format_specs: dict = get_format(CONFIG_FILE_PATH),
    hide: list[str] = get_hide(CONFIG_FILE_PATH),
) -> dict[str, str]:
    d = todo.__dict__
    d.pop('_sa_instance_state', None)
    [d.pop(k, None) for k in hide]
    # from icecream import ic
    # ic(d)
    attr_list_1 = ['id', 'description', 'priority', 'status']
    # attr_list_2 = [
    #     'tags',
    #     'due_date',
    # ]
    # 1
    d_ordered = {k.title(): d[k] for k in attr_list_1 if k in d}
    # 2
    if 'project_id' in d and d['project_id'] is not None:
        project_id = d['project_id']
        with Session(engine) as session:
            project = session.get(Project, project_id)
            assert project is not None
            d_ordered['Project'] = project.name
    elif 'project' in d:
        d_ordered['Project'] = None

    # 3
    # d_ordered |= {k: d[k] for k in attr_list_2}
    # tags
    if 'tags' in d:
        d_ordered['Tags'] = ', '.join(deserialize_tags(d['tags']))
    # due_date
    # typer.secho(type(todo.due_date))
    if 'due_date' in d:
        d_ordered['Due'] = format_datetime(
            todo.due_date,
            full=date_added_full_date,
            date_format=format_specs['due_date'],
        )

    # 4
    # d_ordered |= {'date_added': format_datetime(d['date_added'], date_added_full_date)}
    if 'date_added' in d:
        d_ordered['Added'] = format_datetime(
            todo.date_added,
            full=date_added_full_date,
            date_format=format_specs['date_added'],
        )

    return d_ordered


def _get_todo(
    todo_id,
    session: Session,
    output: bool = False,
    date_added_full: bool = False,
    echo_if_no_matching_todo: bool = True,
) -> Todo:
    todo = session.get(Todo, todo_id)
    if todo is None:
        if echo_if_no_matching_todo:
            typer.secho(f'No to-do with id {todo_id}', fg=typer.colors.RED, err=True)
        raise typer.Exit()
    if output:
        todo_list = [
            todo_to_dict_with_project_name(
                todo, date_added_full, get_format(CONFIG_FILE_PATH)
            )
        ]
        table = tabulate(todo_list, headers='keys')
        typer.secho(table)
    return todo


def export_todo_to_todo_command(todo_id: int) -> str:
    """Export the todo command that can be used to re-construct to todo,
    Only guaranteed to work in POSIX compliant shells."""
    import shlex

    with Session(engine) as session:
        todo = _get_todo(todo_id, session, echo_if_no_matching_todo=False)
    todo_project = todo_to_dict_with_project_name(todo)['project']
    cmd = [
        __app_name__,
        'a',
        todo.description,
        '--priority',
        todo.priority,
        '--status',
        todo.status,
        '--due-date',
        str_self_or_empty(todo.due_date),
        '--date-added',
        str_self_or_empty(todo.date_added),
    ]
    if todo_project:
        cmd.extend(['--project', todo_project])
    if todo.tags:
        tags: list[str] = json.loads(todo.tags)
        for tag in tags:
            cmd.extend(['-t', tag])
    return shlex.join(cmd)
