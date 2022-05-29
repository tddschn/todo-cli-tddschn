#!/usr/bin/env python3

from datetime import datetime
import json
from sqlmodel import Session, select
from .database import engine
from .models import Project, Todo
import typer
from tabulate import tabulate
from . import __app_name__
from .utils import export_todo_to_todo_command

app = typer.Typer(name='utils')


@app.command('export')
def export_todos():
    """Export todos to todo commands that can be used to restore your todo database,
    Only guaranteed to work in POSIX compliant shells."""
    # get all todo ids
    with Session(engine) as session:
        todo_ids: list[int] = [todo.id for todo in session.query(Todo).all()]
    export_commands = '\n'.join(
        export_todo_to_todo_command(todo_id) for todo_id in todo_ids
    )
    typer.secho(export_commands)


# using alembic instead
# https://github.com/tiangolo/sqlmodel/issues/85#issuecomment-917228849=

# @app.command('db-add-date-added-column')
# def add_date_added_column():
#     """Add date_added column to todos table"""
#     with Session(engine) as session:
#         session.exec("ALTER TABLE todos ADD COLUMN date_added DATETIME")
#         session.commit()
#         typer.secho("Done")


@app.command('fill-date-added-column')
def fill_column():
    """fill date_added column with the current time if it's null"""
    with Session(engine) as session:
        session.exec("UPDATE todo SET date_added = datetime('now') WHERE date_added IS NULL")  # type: ignore
        session.commit()
        typer.secho("Done")


@app.callback()
def main():
    """Utility functions"""
