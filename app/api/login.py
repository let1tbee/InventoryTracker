from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app import database, models
from app.repository import login

SessionDep = Annotated[database.Session, Depends(database.get_session)]
router = APIRouter()

@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> models.Token:

    return login.login_for_access_token(form_data, session)


@router.post("/users/")
def post_user(user: models.UsersBase, session: SessionDep):

    return login.post_user(user, session)