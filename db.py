from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated, Generator, Any

db_name = "proyecto.sqlite3"
db_url = f"sqlite:///{db_name}"

engine = create_engine(db_url)

def create_tables(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
