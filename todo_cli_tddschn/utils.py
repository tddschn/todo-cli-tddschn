from datetime import datetime
import json
from sqlmodel import Session, select
from .database import engine
from .models import Project, Todo
import typer
from tabulate import tabulate
from . import __app_name__


def merge_desc(desc_l: list[str]) -> str:
    return ' '.join(desc_l)


def format_datetime(d: datetime, full: bool = False) -> str:
    if full:
        return d.strftime('%Y-%m-%d %H:%M:%S')
    return d.strftime('%Y-%m-%d')


def serialize_tags(tags: list[str]) -> str:
    return json.dumps(tags)


def deserialize_tags(tags_s: str) -> list[str]:
    return json.loads(tags_s)


# def serialize_todo(todo: TodoItem) -> dict:
#     return {
#         'id': todo.id,
#         'description': todo.description,
#         'priority': todo.priority.value,
#         'status': todo.status.value,
#         'project': todo.project,
#         'tags': todo.tags,
#         'due_date': todo.due_date,
#     }


def todo_to_dict_with_project_name(
    todo: Todo, date_added_full_date: bool = False
) -> dict:
    d = todo.__dict__
    d.pop('_sa_instance_state', None)
    # from icecream import ic
    # ic(d)
    attr_list_1 = ['id', 'description', 'priority', 'status']
    attr_list_2 = [
        'tags',
        'due_date',
    ]
    # 1
    d_ordered = {k: d[k] for k in attr_list_1}
    # 2
    if d['project_id'] is not None:
        project_id = d['project_id']
        with Session(engine) as session:
            project = session.get(Project, project_id)
            assert project is not None
            d_ordered['project'] = project.name
    else:
        d_ordered['project'] = None

    # 3
    d_ordered |= {k: d[k] for k in attr_list_2}

    # 4
    d_ordered |= {'date_added': format_datetime(d['date_added'], date_added_full_date)}

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
        todo_list = [todo_to_dict_with_project_name(todo, date_added_full)]
        table = tabulate(todo_list, headers='keys')
        typer.secho(table)
    return todo


def export_todo_command(todo_id: int) -> str:
    """Export the todo command that can be used to re-construct to todo"""
    import shlex

    with Session(engine) as session:
        todo = _get_todo(todo_id, session, echo_if_no_matching_todo=False)
    todo_project = todo_to_dict_with_project_name(todo)['project']
    cmd = [
        __app_name__,
        'a',
        todo.description,
        '-p',
        todo.priority,
        '-s',
        todo.status,
        '-pr',
        todo_project,
        '-t',
        todo.tags,
        '-dd',
        todo.due_date,
        '-da',
        todo.date_added,
    ]
    return shlex.join(cmd)
