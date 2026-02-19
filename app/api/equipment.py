from fastapi import Depends, status, APIRouter
from typing import Annotated
from app import database, models
from app.repository import equipment

SessionDep = Annotated[database.Session, Depends(database.get_session)]

router = APIRouter(prefix="/equipment",
                   tags=["equipment"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment(equip: models.Equipment, session: SessionDep):
    return equipment.create_equipment(equip, session)

@router.get("/{equip_id}")
def get_equipment(equip_id: int, session: SessionDep):
    return equipment.get_equipment(equip_id, session)

@router.get("/")
def get_equipments(session: SessionDep, offset: int = 0, limit: int = 10):
    return equipment.get_equipments(session, offset, limit)

@router.delete("/{emp_id}")
def delete_equipment(emp_id: int, session: SessionDep):
    return equipment.delete_equipment(emp_id, session)

@router.patch("/{emp_id}")
def update_equipment(emp_id: int, equip: models.EquipmentUpdate, session: SessionDep):
    return equipment.update_equipment(emp_id, equip, session)