from sqlmodel import SQLModel, create_engine
from .config import DEFAULT_DB_FILE_PATH

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{str(DEFAULT_DB_FILE_PATH)}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
