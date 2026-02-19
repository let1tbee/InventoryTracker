from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session, StaticPool
import pytest
from main import app
from app.database import get_session

test_equipment = [{
        "name": "laptop",
        "s_n": "0001"
        },
        {
        "name": "laptop",
        "s_n": "0002"
        },
        {
        "name": "laptop",
        "s_n": "0003"
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

@pytest.fixture
def create_test_employee():
    client.post("/employees/", json={
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "email": "test@test"
        })


@pytest.mark.parametrize("equipment", test_equipment)
def test_create_equipment(equipment):
    response = client.post("/equipment/", json=equipment)
    assert response.status_code == 201

def test_get_equipments():
    response = client.get("/equipment/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_equipment)
    for i in range(len(test_equipment)):
        assert data[i]["name"] == test_equipment[i]["name"]
        assert data[i]["s_n"] == test_equipment[i]["s_n"]
        assert data[i]["status"] == "available"

def test_get_equipment():
    response = client.get("/equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_equipment[0]["name"]
    assert data["s_n"] == test_equipment[0]["s_n"]

@pytest.mark.parametrize("equipment", test_equipment)
def test_search_equipments(equipment):
    link = "/equipment/search/?name="+equipment["name"]+"&s_n="+equipment["s_n"]
    response = client.get(link)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == equipment["name"]
    assert data[0]["s_n"] == equipment["s_n"]

def test_assign_equipment(create_test_employee):
    response = client.patch("/equipment/assign/1?assignee_id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["assigned_to"] == 1

def test_update_equipment():
    response = client.patch("/equipment/1", json={"s_n" : "0007"})
    assert response.status_code == 200
    data = response.json()
    assert data["s_n"] == "0007"

def test_delete_equipment():
    response = client.delete("/equipment/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {"ok" : True}
    response_del = client.get("/equipment/")
    assert response_del.status_code == 200
    data_del = response_del.json()
    assert len(data_del) == len(test_equipment) - 1


