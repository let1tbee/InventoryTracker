from app import models
from sqlmodel import Session, select
from fastapi import HTTPException, status

def create_employee(employee: models.EmployeesBase, session: Session):
    employee_db = models.Employees.model_validate(employee)
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db

def get_employee(emp_id: int, session: Session):
    employee = session.get(models.Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    return employee

def get_employees(session: Session, offset: int, limit: int):
    employees = session.exec(select(models.Employees).offset(offset).limit(limit)).all()
    return employees

def get_assigned_equipment(emp_id: int, session: Session):
    employee = session.get(models.Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    if not employee.equipment_list:
        return {"equipment_list": "No assigned equipment"}
    return employee.equipment_list

def search_employees(session, first_name, last_name, email, offset, limit):
    statement = select(models.Equipment)

    if first_name is not None:
        statement = statement.where(models.Equipment.first_name == first_name)
    if last_name is not None:
        statement = statement.where(models.Equipment.s_n == last_name)
    if email is not None:
        statement = statement.where(models.Equipment.status == email)

    statement = statement.offset(offset).limit(limit)
    equips = session.exec(statement).all()
    if not equips:
        return {"result": "No equipments found"}
    return equips

def delete_employee(emp_id: int, session: Session):
    employee = session.get(models.Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    session.delete(employee)
    session.commit()
    return {"ok" : True}

def update_employee(emp_id: int, employee: models.EmployeeUpdate, session: Session):
    employee_db = session.get(models.Employees, emp_id)
    if not employee_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    employee_data = employee.model_dump(exclude_unset=True)
    employee_db.sqlmodel_update(employee_data)
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db