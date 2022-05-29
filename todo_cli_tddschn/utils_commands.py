#!/usr/bin/env python3

from datetime import datetime
import json
from sqlmodel import Session, select
from .database import engine
from .models import Project, Todo
import typer
from tabulate import tabulate
from . import __app_name__
from .utils import export_todo_command

app = typer.Typer(name='utils')


@app.command('export')
def export_todos():
    """Export todos to todo commands that can be used to restore your todo database"""
    # get all todo ids
    with Session(engine) as session:
        todo_ids: list[int] = [todo.id for todo in session.query(Todo).all()]
    export_commands = '\n'.join(export_todo_command(todo_id) for todo_id in todo_ids)
    typer.secho(export_commands)
