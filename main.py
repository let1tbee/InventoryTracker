from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import create_engine, SQLModel, Field, Session
from contextlib import asynccontextmanager
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
engine = create_engine(settings.DB_URL, echo=True)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(title='Inventory Tracker',
    description='A tool that is used to track equipment within the company.',
    summary="Backend portfolio project.",
    version='0.0.1',
    lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Welcome to Inventory Tracker API!"}

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero





