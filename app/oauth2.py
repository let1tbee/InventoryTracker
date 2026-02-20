from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from sqlmodel import select, Session
from typing import Annotated
from app import models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from app import database
import jwt

SECRET_KEY = "a6ca255694fac63b88e89gr8m0j4caa6cfd3e818166b7a9563b93f7009d25e07"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SessionDep = Annotated[database.Session, Depends(database.get_session)]

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(select(models.Users).where(models.Users.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(models.Users).where(models.Users.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt