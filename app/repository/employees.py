from app import models
from sqlmodel import Session, select
from fastapi import HTTPException, status

def create_employee(employee: models.EmployeesBase, session: Session):
    db_employee = models.Employees.model_validate(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

def get_employee(emp_id: int, session: Session):
    employee = session.get(models.Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    return employee

def get_employees(session: Session, offset: int, limit: int):
    employees = session.exec(select(models.Employees).offset(offset).limit(limit)).all()
    return employees

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