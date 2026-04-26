from fastapi import APIRouter, Depends

from db.db import get_session
from schemas.user import UserRead, UserUpdate
from services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/users", response_model=list[UserRead])
def users_get(session=Depends(get_session)):
    return user_service.get_all(session)

@router.get("/users/{user_id}", response_model=UserRead)
def user_get(user_id: int, session=Depends(get_session)) -> UserRead:
    return user_service.get_by_id(user_id, session)

@router.patch("/users/{user_id}", response_model=UserRead)
def user_update(user_id: int, user: UserUpdate, session=Depends(get_session)):
    return user_service.update(user_id, user, session)
