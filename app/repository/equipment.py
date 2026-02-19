from app import models
from sqlmodel import Session, select
from fastapi import HTTPException, status

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

def get_equipments(session: Session, offest: int, limit: int):
    equips = session.exec(select(models.Equipment).offset(offset).limit(limit)).all()
    return equips

def delete_equipment(equip_id: int, session: Session):
    equip = session.get(models.Equipment, equip_id)
    if not equip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Equipment with id {equip_id} not found")
    session.delete(equip)
    session.commit()
    session.refresh(equip)
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

