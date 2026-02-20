import pytest

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


@pytest.fixture
def create_assigned_equipment(client):
    client.post("/equipment/", json={
        "name": "laptop",
        "s_n": "0001"
        })
    client.patch("/equipment/assign/1?assignee_id=1")

@pytest.mark.parametrize("employee", test_employees)
def test_create_employee(employee, client):
    response = client.post("/employees/", json=employee)
    assert response.status_code == 201


def test_get_employees(client):
    response = client.get("/employees/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_employees)
    for i in range(len(test_employees)):
        assert data[i]["first_name"] == test_employees[i]["first_name"]
        assert data[i]["last_name"] == test_employees[i]["last_name"]
        assert data[i]["email"] == test_employees[i]["email"]

def test_get_employee(client):
    response = client.get("/employees/1")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == test_employees[0]["first_name"]
    assert data["last_name"] == test_employees[0]["last_name"]
    assert data["email"] == test_employees[0]["email"]

@pytest.mark.parametrize("employee", test_employees)
def test_search_equipments(employee,client):
    link = "/employees/search/?first_name="+employee["first_name"]+"&last_name="+employee["last_name"]+"&email="+employee["email"]
    response = client.get(link)
    assert response.status_code == 200
    data = response.json()
    assert data[0]["first_name"] == employee["first_name"]
    assert data[0]["last_name"] == employee["last_name"]
    assert data[0]["email"] == employee["email"]

def test_get_assigned_equipment(create_assigned_equipment,client):
    response = client.get("/employees/equipment/1")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data

def test_update_employee(client):
    response = client.patch("/employees/1", json={"first_name" : "changed_first_name"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "changed_first_name"

def test_delete_employee(client):
    response = client.delete("/employees/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {'ok': True}
    response_del = client.get("/employees/")
    assert response_del.status_code == 200
    data_del = response_del.json()
    assert len(data_del) == len(test_employees) - 1









