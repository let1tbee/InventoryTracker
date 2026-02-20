import pytest
from app import models

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

single_test_employee = {
            "first_name": "test_first_name3",
            "last_name": "test_last_name3",
            "email": "test3@test",
            }

test_equipment = [{
        "name": "laptop",
        "s_n": "0001"
        }]

@pytest.fixture()
def fill_test_tables(setup_session):
    for i in test_employees:
        empl_db = models.Employees.model_validate(i)
        setup_session.add(empl_db)

    for i in test_equipment:
        equip_db = models.Equipment.model_validate(i)
        empl_db = setup_session.get(models.Employees, 1)
        setup_session.add(equip_db)
        equip_db.assignee = empl_db
        equip_db.status = models.ItemStatus.ASSIGNED

    setup_session.commit()

@pytest.mark.usefixtures("fill_test_tables")
class TestEmployees:

    def test_create_employee(self, authorized_client):
        response = authorized_client.post("/employees/", json=single_test_employee)
        assert response.status_code == 201

    def test_get_employee(self, client):
        response = client.get("/employees/1")
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == test_employees[0]["first_name"]
        assert data["last_name"] == test_employees[0]["last_name"]
        assert data["email"] == test_employees[0]["email"]

    def test_get_employees(self, client):
        response = client.get("/employees/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(test_employees)
        for i in range(len(test_employees)):
            assert data[i]["first_name"] == test_employees[i]["first_name"]
            assert data[i]["last_name"] == test_employees[i]["last_name"]
            assert data[i]["email"] == test_employees[i]["email"]

    @pytest.mark.parametrize("employee", test_employees)
    def test_search_equipments(self, employee, client):
        link = "/employees/search/?first_name="+employee["first_name"]+"&last_name="+employee["last_name"]+"&email="+employee["email"]
        response = client.get(link)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["first_name"] == employee["first_name"]
        assert data[0]["last_name"] == employee["last_name"]
        assert data[0]["email"] == employee["email"]

    def test_get_assigned_equipment(self, client):
        response = client.get("/employees/equipment/1")
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert data

    def test_update_employee(self, authorized_client):
        response = authorized_client.patch("/employees/1", json={"first_name" : "changed_first_name"})
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "changed_first_name"

    def test_delete_employee(self, authorized_client):
        response = authorized_client.delete("/employees/1")
        assert response.status_code == 200
        data = response.json()
        assert data == {'ok': True}
        response_del = authorized_client.get("/employees/")
        assert response_del.status_code == 200
        data_del = response_del.json()
        assert len(data_del) == len(test_employees) - 1









