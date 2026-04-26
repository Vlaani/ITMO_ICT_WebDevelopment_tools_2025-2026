from fastapi import HTTPException, Depends
from sqlmodel import select
from typing import Annotated

from models.user import User
from schemas.user import UserCreate, UserLogin, UserRead, UserUpdate, UserReadFull
from services.security_service import SecurityService
from fastapi.security import OAuth2PasswordBearer
from db.db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

class AuthService:
    def __init__(self):
        self.security_service = SecurityService()

    def register(self, user: UserCreate, session):
        existing_user = session.exec(select(User).where(User.login == user.login)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already exists")

        existing_email = session.exec(select(User).where(User.email == user.email)).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

        user_data = user.model_dump()
        user_data["password"] = self.security_service.get_password_hash(user_data["password"])
        db_user = User.model_validate(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return UserRead.model_validate(db_user)

    def login(self, payload: UserLogin, session):
        user = session.exec(select(User).where(User.login == payload.login)).first()
        if not user or not self.security_service.verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid login or password")

        access_token = self.security_service.create_access_token(data=f"{user.id}")
        return access_token

    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_session)):   
        return self.get_by_token(token, session)

    def get_by_token(self, token, session) -> UserReadFull:
        if not token:
            raise HTTPException(status_code=401, detail="Empty token")
        
        data = self.security_service.decode_access_token(token)
        user_id = data
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        db_user = session.get(User, int(user_id))
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    
    def update_user(self, db_user, user: UserUpdate, session):
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)

        for key, value in user_data.items():
            if key == "password":
                value = self.security_service.get_password_hash(value)
            setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
