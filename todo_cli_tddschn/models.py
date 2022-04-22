from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class TodoBase(SQLModel):
    description: str
    priority: str = Field(default='medium')
    status: str = Field(default='todo')
    tags: str | None
    due_date: datetime | None
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project: Optional['Project'] = Relationship(back_populates='todos')


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int


class ProjectBase(SQLModel):
    name: str = Field(index=True)


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    todos: Todo | None = Relationship(back_populates='project')


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int