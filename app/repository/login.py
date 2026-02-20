from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from datetime import  timedelta
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app import models, oauth2

ACCESS_TOKEN_EXPIRE_MINUTES = 30

def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session
) -> models.Token:
    user = oauth2.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")

def post_user(user: models.UsersBase, session: Session):
    user_data = user.model_dump()
    user_data["password"] = oauth2.get_password_hash(user.password)
    user_db = models.Users(**user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db