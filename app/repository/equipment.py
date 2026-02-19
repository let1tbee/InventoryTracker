from app import models
from sqlmodel import Session, select
from fastapi import HTTPException, status

def create_equipment(equip: models.Equipment, session: Session):
    pass

def get_equipment(equip_id: int, session: Session):
    pass

def get_equipements(session: Session, offest: int, limit: int):
    pass

def delete_equipment(equip_id: int, session: Session):
    pass

def update_equipment(equip_id: int, equip: models.EquipmentUpdate, session: Session):
    pass
