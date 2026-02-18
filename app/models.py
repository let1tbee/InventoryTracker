from sqlmodel import SQLModel, Field

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