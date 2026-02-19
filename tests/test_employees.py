import pytest
from sqlmodel import create_engine, SQLModel, Session, StaticPool
from fastapi.testclient import TestClient
from main import app
from app.database import get_session

test_employees = [{
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "email": "test@test",
        },
        {
        "first_name": "test_first_name1",
        "last_name": "test_last_name1",
        "email": "test1@test",
        },
        {
        "first_name": "test_first_name2",
        "last_name": "test_last_name2",
        "email": "test2@test",
        }]

sqlite_url = f"sqlite:///:memory:"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, poolclass=StaticPool)
SQLModel.metadata.create_all(engine)

def override_get_session():
    with Session(engine) as session:
        yield session

client = TestClient(app)
app.dependency_overrides[get_session] = override_get_session

@pytest.mark.parametrize("employee", test_employees)
def test_create_employee(employee):
    response = client.post("/employees/", json=employee)
    assert response.status_code == 201


def test_get_employees():
    response = client.get("/employees/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_employees)
    for i in range(len(test_employees)):
        assert data[i]["first_name"] == test_employees[i]["first_name"]
        assert data[i]["last_name"] == test_employees[i]["last_name"]
        assert data[i]["email"] == test_employees[i]["email"]

def test_get_employee():
    response = client.get("/employees/1")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_employees[0]["first_name"]
    assert data["last_name"] == test_employees[0]["last_name"]
    assert data["email"] == test_employees[0]["email"]

def test_update_employee():
    response = client.patch("/employees/1", json={"first_name" : "changed_first_name"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "changed_first_name"

def test_delete_employee():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {'ok': True}
    response_del = client.get("/employees/")
    assert response_del.status_code == 200
    data_del = response_del.json()
    assert len(data_del) == len(test_employees) - 1






