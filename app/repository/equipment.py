from app import models
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models import ItemStatus


def create_equipment(equip: models.EquipmentBase, session: Session):
    db_equip = models.Equipment.model_validate(equip)
    session.add(db_equip)
    session.commit()
    session.refresh(db_equip)
    return db_equip

def get_equipment(equip_id: int, session: Session):
    equip = session.get(models.Equipment, equip_id)
    if not equip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Equipment with id {equip_id} not found")
    return equip

def get_equipments(session: Session, offset: int, limit: int):
    equips = session.exec(select(models.Equipment).offset(offset).limit(limit)).all()
    return equips

def search_equipments(session, name, s_n, equip_status, offset, limit):
    statement = select(models.Equipment)

    if name is not None:
        statement = statement.where(models.Equipment.name == name)
    if s_n is not None:
        statement = statement.where(models.Equipment.s_n == s_n)
    if equip_status is not None:
        statement = statement.where(models.Equipment.status == equip_status)

    statement = statement.offset(offset).limit(limit)
    equips = session.exec(statement).all()
    if not equips:
        return {"result": "No equipments found"}
    return equips

def delete_equipment(equip_id: int, session: Session):
    equip = session.get(models.Equipment, equip_id)
    if not equip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Equipment with id {equip_id} not found")
    session.delete(equip)
    session.commit()
    return {"ok" : True}

def update_equipment(equip_id: int, equip: models.EquipmentUpdate, session: Session):
    equip_db = session.get(models.Equipment, equip_id)
    if not equip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Equipment with id {equip_id} not found")
    equip_data = equip.model_dump(exclude_unset=True)
    equip_db.sqlmodel_update(equip_data)
    session.add(equip_db)
    session.commit()
    session.refresh(equip_db)
    return equip_db

def assign_equipment(equip_id: int, assignee_id: int, session: Session):
    equip = session.get(models.Equipment, equip_id)
    if not equip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Equipment with id {equip_id} not found")
    if assignee_id:
        employee = session.get(models.Employees, assignee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {assignee_id} not found")
        equip.assignee = employee
        equip.status = ItemStatus.ASSIGNED
    else:
        equip.assignee = None
        equip.status = ItemStatus.AVAILABLE
    session.commit()
    session.refresh(equip)
    return equip

