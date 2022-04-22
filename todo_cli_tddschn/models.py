from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class TodoBase(SQLModel):
    description: str
    priority: str = Field(default='medium')
    status: str = Field(default='todo')
    tags: str | None
    due_date: datetime | None
    project_id: int | None


class Todo(TodoBase, table=True):
    id: int | None = Field(primary_key=True)
    project: Optional['Project'] = Relationship(back_populates='todos')
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")


class ProjectBase(SQLModel):
    name: str


class Project(ProjectBase, table=True):
    id: int | None = Field(primary_key=True)
    todos: Todo | None = Relationship(back_populates='project')
