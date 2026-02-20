from sqlmodel import create_engine, SQLModel, Session
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings

engine = create_engine(settings.DB_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()
