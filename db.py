from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated, Generator, Any
import os



DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///pets1.sqlite3")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_tables(app=None):
    SQLModel.metadata.create_all(engine)
    yield


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
