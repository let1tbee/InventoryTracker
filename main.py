from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import create_engine, SQLModel, Field, Session, select
from contextlib import asynccontextmanager
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
engine = create_engine(settings.DB_URL, echo=True)

class EmployeesBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str | None = Field(default=None, index=True)

class Employees(EmployeesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class EmployeeUpdate(EmployeesBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(title='Inventory Tracker',
    description='A tool that is used to track equipment within the company.',
    summary="Backend portfolio project.",
    version='0.0.1',
    lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Welcome to Inventory Tracker API!"}

@app.post("/employees/", tags = ["employees"], response_model=EmployeesBase, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeesBase, session: SessionDep):
    db_employee = Employees.model_validate(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

@app.get("/employees/{emp_id}", tags = ["employees"], response_model=EmployeesBase)
def get_employee(emp_id: int, session: SessionDep):
    employee = session.get(Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    return employee

@app.get("/employees/", tags = ["employees"])
def get_employees(session: SessionDep, limit: int = 10):
    employees = session.exec(select(Employees).limit(limit)).all()
    return employees

@app.delete("/employees/{emp_id}", tags = ["employees"])
def delete_employee(emp_id: int, session: SessionDep):
    employee = session.get(Employees, emp_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    session.delete(employee)
    session.commit()
    return {"ok" : True}

@app.patch("/employees/{emp_id}", tags = ["employees"], response_model=EmployeesBase)
def update_employee(emp_id: int, employee: EmployeeUpdate, session: SessionDep):
    employee_db = session.get(Employees, emp_id)
    if not employee_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {emp_id} not found")
    employee_data = employee.model_dump(exclude_unset=True)
    employee_db.sqlmodel_update(employee_data)
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db


