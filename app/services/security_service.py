import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


class SecurityService:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET", "dev-secret-change-me")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.token_ttl_seconds = int(os.getenv("JWT_TTL_SECONDS", "3600"))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)

    def create_access_token(self, data: str):
        expire = datetime.now(timezone.utc) + timedelta(seconds=self.token_ttl_seconds)
        to_encode = {"sub": data, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token) -> Any | None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            print(payload)
        except InvalidTokenError:
            raise credentials_exception

        if "sub" not in payload:
            raise ValueError("Token payload does not contain subject.")

        return payload.get("sub")
