from typing import Optional

from fastapi import HTTPException, Header, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.models import UserLogin
from ..db.db import get_session

import jwt
from jwt import PyJWTError
import os
import secrets
import hashlib


class Auth:
    def __init__(self):
        self.__secret_key = os.getenv("SECRET_KEY")
        self.__algorithm = "HS256"
        self.__salt = os.getenv("SALT")
        # self.__expires_in = 3600

    def create_token(self, email: str) -> str:
        return jwt.encode(
            {"email": email},
            self.__secret_key,
            algorithm=self.__algorithm,
        )

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def hash_password(self, password: str) -> str:
        salted_password = password + self.__salt
        return hashlib.sha256(salted_password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.hash_password(password) == hashed_password


async def get_current_user(session: AsyncSession, email: str):
    query = select(UserLogin).where(UserLogin.email == email)
    result = await session.execute(query)
    return result.scalars().first()


async def add_user(
    session: AsyncSession, email: str, password: str
) -> Optional[UserLogin]:
    try:
        result = await session.execute(
            select(UserLogin).filter(UserLogin.email == email)
        )
        existing_user = result.scalars().first()

        if existing_user:
            return None

        auth = Auth()
        hashed_password = auth.hash_password(password)

        new_user = UserLogin(email=email, hashed_password=hashed_password)

        session.add(new_user)
        await session.commit()

        return new_user

    except SQLAlchemyError as e:
        await session.rollback()
        raise e


auth = Auth()


async def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session),
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.split(" ")[-1]

    try:
        payload = auth.verify_token(token)

        email = payload.get("email")

        if email is None:
            raise HTTPException(
                status_code=401, detail="Invalid token: email not found"
            )

        query = select(UserLogin).where(UserLogin.email == email)
        result = await session.execute(query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
