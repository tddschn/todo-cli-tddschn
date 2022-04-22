from sqlmodel import SQLModel, create_engine, Session
from .config import DEFAULT_DB_FILE_PATH
from .models import Project, Todo
from . import _DEBUG

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{str(DEFAULT_DB_FILE_PATH)}"

engine = create_engine(sqlite_url, echo=bool(_DEBUG))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_project_with_name(project_name: str) -> Project:
    """
    get the project with the name project_name, or create one if it doesn't exist
    """
    with Session(engine) as session:
        project = session.query(Project).filter_by(name=project_name).first()
        if project is None:
            project = Project(name=project_name)
            session.add(project)
            session.commit()
            session.refresh(project)
    return project
