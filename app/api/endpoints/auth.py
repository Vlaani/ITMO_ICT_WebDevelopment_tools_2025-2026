from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import UserRead, UserCreate, UserLogin, UserUpdate, Token, UserReadFull
from db.db import get_session
from services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def register(user: UserCreate, session=Depends(get_session)):
    auth_service.register(user, session)
    access_token = auth_service.login(UserLogin(login=user.username, password=user.password), session)
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session=Depends(get_session)):
    access_token = auth_service.login(UserLogin(login=form_data.username, password=form_data.password), session)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me")
def users_me(current_user: Annotated[UserReadFull, Depends(auth_service.get_current_user)]):
    return current_user

@router.patch("/me/update", response_model=UserRead)
def user_update(current_user: Annotated[UserRead, Depends(auth_service.get_current_user)], user: UserUpdate, session=Depends(get_session)):
    return auth_service.update_user(current_user, user, session)