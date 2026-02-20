from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session, StaticPool
from app.database import get_session
from main import app
import pytest

@pytest.fixture(scope ="module")
def engine():
    sqlite_url = f"sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args, poolclass=StaticPool)
    return engine

@pytest.fixture(scope ="module")
def setup_tables(engine):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope ="module")
def setup_session(engine, setup_tables):
    with Session(engine) as session:
        yield session

@pytest.fixture(scope ="module")
def client(setup_session):
    def override_get_session():
        return setup_session

    app.dependency_overrides[get_session] = override_get_session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()