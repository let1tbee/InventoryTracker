from fastapi import Depends, status, APIRouter, Query
from typing import Annotated
from app import database, models, oauth2
from app.repository import employees

SessionDep = Annotated[database.Session, Depends(database.get_session)]

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: models.EmployeesBase,
    session: SessionDep,
    current_user: Annotated[models.Users, Depends(oauth2.get_current_user)],
):
    return employees.create_employee(employee, session)


@router.get("/{emp_id}")
def get_employee(emp_id: int, session: SessionDep):
    return employees.get_employee(emp_id, session)


@router.get("/")
def get_employees(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10
):
    return employees.get_employees(session, offset, limit)


@router.get("/search/")
def search_employees(
    session: SessionDep,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return employees.search_employees(
        session, first_name, last_name, email, offset, limit
    )


@router.get("/equipment/{emp_id}")
def get_assigned_equipment(emp_id: int, session: SessionDep):
    return employees.get_assigned_equipment(emp_id, session)


@router.delete("/{emp_id}")
def delete_employee(
    emp_id: int,
    session: SessionDep,
    current_user: Annotated[models.Users, Depends(oauth2.get_current_user)],
):
    return employees.delete_employee(emp_id, session)


@router.patch("/{emp_id}")
def update_employee(
    emp_id: int,
    employee: models.EmployeeUpdate,
    session: SessionDep,
    current_user: Annotated[models.Users, Depends(oauth2.get_current_user)],
):
    return employees.update_employee(emp_id, employee, session)
