from http import HTTPStatus
from starlette import status
from typing import Annotated
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from src.config import SECRET_KEY
from .database import collection_name
from .models import individual_serial

ALGORITHM = "HS256"

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.get('/')
async def index(user: Annotated[dict, Depends(get_current_user)]):
    return {"message": "Welcome"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token(user["username"], user["id"], timedelta(minutes=10080))

    return {"accessToken": token, "tokenType": "Bearer"}


def authenticate_user(username: str, password: str):
    user = collection_name.find_one({"email": username})
    if not user:
        return False
    if not bcrypt_context.verify(password, user["password"]):
        return False
    return individual_serial(user)


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, "id": user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
