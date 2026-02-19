from fastapi import Depends, status, APIRouter
from typing import Annotated
from app import database, models
from app.repository import employees

SessionDep = Annotated[database.Session, Depends(database.get_session)]

router = APIRouter(prefix="/equipment",
                   tags=["equipment"])