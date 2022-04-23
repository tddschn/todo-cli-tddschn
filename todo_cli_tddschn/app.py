#!/usr/bin/env python3

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from .models import Project, Todo, ProjectCreate, ProjectRead, TodoCreate, TodoRead, ProjectUpdate, TodoUpdate, ProjectReadWithTodos, TodoReadWithProject
from .database import engine


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


@app.post("/todos/", response_model=TodoRead)
def create_todo(*, session: Session = Depends(get_session), todo: TodoCreate):
    db_todo = Todo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=list[TodoRead])
def read_todos(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return todos


@app.get("/todos/{todo_id}", response_model=TodoReadWithProject)
def read_todo(*, session: Session = Depends(get_session), todo_id: int):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todos/{todo_id}", response_model=TodoRead)
def update_todo(*,
                session: Session = Depends(get_session),
                todo_id: int,
                todo: TodoUpdate):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todos/{todo_id}")
def delete_todo(*, session: Session = Depends(get_session), todo_id: int):

    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}


@app.post("/projects/", response_model=ProjectRead)
def create_project(*,
                   session: Session = Depends(get_session),
                   project: ProjectCreate):
    db_project = Project.from_orm(project)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@app.get("/projects/", response_model=list[ProjectRead])
def read_projects(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
):
    projects = session.exec(select(Project).offset(offset).limit(limit)).all()
    return projects


@app.get("/projects/{project_id}", response_model=ProjectReadWithTodos)
def read_project(*, project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    *,
    session: Session = Depends(get_session),
    project_id: int,
    project: ProjectUpdate,
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}")
def delete_project(*, session: Session = Depends(get_session),
                   project_id: int):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}
