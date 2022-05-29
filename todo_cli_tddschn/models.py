from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class TodoBase(SQLModel):
    description: str
    priority: str = Field(default='medium')
    status: str = Field(default='todo')
    tags: str | None
    due_date: datetime | None
    date_added: datetime | None
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project: Optional['Project'] = Relationship(back_populates='todos')


class TodoUpdate(SQLModel):
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: list[str] | None = None
    due_date: datetime | None = None
    date_added: datetime | None = None
    project_id: Optional[int] = None


class TodoCreate(TodoBase):
    date_added: datetime | None = datetime.now()


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


class ProjectUpdate(SQLModel):
    name: Optional[str] = None


class TodoReadWithProject(TodoRead):
    project: Optional[ProjectRead] = None


class ProjectReadWithTodos(ProjectRead):
    todos: list[TodoRead] = []
