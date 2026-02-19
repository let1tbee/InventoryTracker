from fastapi import Depends, status, APIRouter, Query
from typing import Annotated
from app import database, models
from app.models import ItemStatus
from app.repository import equipment

SessionDep = Annotated[database.Session, Depends(database.get_session)]

router = APIRouter(prefix="/equipment",
                   tags=["equipment"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment(equip: models.EquipmentBase, session: SessionDep):
    return equipment.create_equipment(equip, session)

@router.get("/{equip_id}")
def get_equipment(equip_id: int, session: SessionDep):
    return equipment.get_equipment(equip_id, session)

@router.get("/")
def get_equipments(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    return equipment.get_equipments(session, offset, limit)

@router.get("/search/")
def search_equipments(
        session: SessionDep,
        name: str | None = None,
        s_n: str | None = None,
        equip_status: ItemStatus | None = None,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 10
        ):
    return equipment.search_equipments(session, name, s_n, equip_status, offset, limit)

@router.delete("/{equip_id}")
def delete_equipment(equip_id: int, session: SessionDep):
    return equipment.delete_equipment(equip_id, session)

@router.patch("/{equip_id}")
def update_equipment(equip_id: int, equip: models.EquipmentUpdate, session: SessionDep):
    return equipment.update_equipment(equip_id, equip, session)

@router.patch("/assign/{equip_id}")
def assign_equipment(equip_id: int, assignee_id: int, session: SessionDep):
    return equipment.assign_equipment(equip_id, assignee_id, session)
