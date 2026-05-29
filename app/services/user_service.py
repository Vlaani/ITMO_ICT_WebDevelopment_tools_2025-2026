from fastapi import HTTPException
from sqlmodel import select

from models.user import User
from schemas.user import UserUpdate
from services.security_service import SecurityService


class UserService:
    def __init__(self):
        self.security_service = SecurityService()

    def get_all(self, session):
        return session.exec(select(User)).all()

    def get_by_id(self, user_id: int, session):
        return session.get(User, user_id)

    def update(self, user_id: int, user: UserUpdate, session):
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.model_dump(exclude_unset=True)
        if "email" in user_data:
            existing_email = session.exec(
                select(User).where((User.email == user_data["email"]) & (User.id != user_id))
            ).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already exists")

        if "password" in user_data:
            user_data["password"] = self.security_service.get_password_hash(user_data["password"])

        for key, value in user_data.items():
            setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
