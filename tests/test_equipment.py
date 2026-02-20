import pytest
from app import models

test_equipment = [
    {"name": "laptop", "s_n": "0001"},
    {"name": "laptop", "s_n": "0002"},
    {"name": "laptop", "s_n": "0003"},
]

single_test_equipment = {"name": "laptop", "s_n": "0004"}

test_employees = [
    {
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "email": "test@test",
    }
]


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
class TestEquipment:
    def test_create_equipment(self, authorized_client):
        response = authorized_client.post("/equipment/", json=single_test_equipment)
        assert response.status_code == 201

    def test_get_equipment(self, client):
        response = client.get("/equipment/1")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_equipment[0]["name"]
        assert data["s_n"] == test_equipment[0]["s_n"]

    def test_get_equipments(self, client):
        response = client.get("/equipment/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(test_equipment)
        for i in range(len(test_equipment)):
            assert data[i]["name"] == test_equipment[i]["name"]
            assert data[i]["s_n"] == test_equipment[i]["s_n"]

    @pytest.mark.parametrize("equipment", test_equipment)
    def test_search_equipments(self, equipment, client):
        link = f"/equipment/search/?name={equipment['name']}&s_n={equipment['s_n']}"
        response = client.get(link)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["name"] == equipment["name"]
        assert data[0]["s_n"] == equipment["s_n"]

    def test_update_equipment(self, authorized_client):
        response = authorized_client.patch("/equipment/1", json={"s_n": "0007"})
        assert response.status_code == 200
        data = response.json()
        assert data["s_n"] == "0007"

    def test_delete_equipment(self, authorized_client):
        response = authorized_client.delete("/equipment/1")
        assert response.status_code == 200
        data = response.json()
        assert data == {"ok": True}
        response_del = authorized_client.get("/equipment/")
        assert response_del.status_code == 200
        data_del = response_del.json()
        assert len(data_del) == len(test_equipment) - 1

    def test_assign_equipment(self, authorized_client):
        response = authorized_client.patch("/equipment/assign/1?assignee_id=1")
        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to"] == 1
