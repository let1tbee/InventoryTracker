from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session, StaticPool
from app.database import get_session
from app.models import Users
from app.oauth2 import get_password_hash
from main import app
import pytest

@pytest.fixture()
def engine():
    sqlite_url = f"sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args, poolclass=StaticPool)
    return engine

@pytest.fixture()
def setup_tables(engine):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def setup_session(engine, setup_tables):
    with Session(engine) as session:
        yield session

@pytest.fixture()
def client(setup_session):
    def override_get_session():
        return setup_session

    app.dependency_overrides[get_session] = override_get_session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def authorized_client(client, setup_session):
    test_user = Users(
        username="test_admin",
        password=get_password_hash("secret_pass")
    )
    setup_session.add(test_user)
    setup_session.commit()

    login_data = {
        "username": "test_admin",
        "password": "secret_pass"
    }
    response = client.post("/token", data=login_data)

    token = response.json()["access_token"]

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client