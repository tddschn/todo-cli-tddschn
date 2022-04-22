from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel


class TodoBase(SQLModel):
    description: str
    priority: str = Field(default='medium')
    status: str = Field(default='todo')
    tags: str | None
    due_date: datetime | None
    project_id: int | None


class Todo(TodoBase, table=True):
    id: int | None
    project: 'Project' | None = Relationship(back_populates='todos')


class ProjectBase(SQLModel):
    name: str


class Project(ProjectBase, table=True):
    id: int | None
    todos: Todo | None = Relationship(back_populates='project')
