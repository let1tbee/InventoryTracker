from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class ItemStatus(str, Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"

class EmployeesBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str | None = Field(unique=True, default=None, index=True)

class Employees(EmployeesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    equipment_list: list["Equipment"] | None = Relationship(back_populates="assignee")

class EmployeeUpdate(EmployeesBase):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class EquipmentBase(SQLModel):
    name: str = Field(index=True)
    s_n: str = Field(unique=True,index=True)

class Equipment(EquipmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: ItemStatus = Field(default=ItemStatus.AVAILABLE, index=True)

    assigned_to: int | None = Field(default=None, index=True, foreign_key="employees.id")
    assignee: Employees | None = Relationship(back_populates="equipment_list")

class EquipmentUpdate(EquipmentBase):
    name: str | None = None
    s_n: str | None = None
    status: ItemStatus | None = None
    assigned_to: int | None = None



