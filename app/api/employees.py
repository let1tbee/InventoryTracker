from fastapi import Depends, status, APIRouter
from typing import Annotated
from app import database, models
from app.repository import employees

SessionDep = Annotated[database.Session, Depends(database.get_session)]

router = APIRouter(prefix="/employees",
                   tags=["employees"])

@router.post("/", response_model=models.EmployeesBase, status_code=status.HTTP_201_CREATED)
def create_employee(employee: models.EmployeesBase, session: SessionDep):
    return employees.create_employee(employee, session)

@router.get("/{emp_id}")
def get_employee(emp_id: int, session: SessionDep):
    return employees.get_employee(emp_id, session)

@router.get("/",)
def get_employees(session: SessionDep, offset: int = 0, limit: int = 10):
    return employees.get_employees(session, offset, limit)

@router.delete("/{emp_id}")
def delete_employee(emp_id: int, session: SessionDep):
    return employees.delete_employee(emp_id, session)

@router.patch("/{emp_id}")
def update_employee(emp_id: int, employee: models.EmployeeUpdate, session: SessionDep):
    return employees.update_employee(emp_id, employee, session)