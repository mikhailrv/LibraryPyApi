# app/auth/services/auth_service.py
from app.auth.models import User
from sqlmodel import select
from app.database.db import AsyncSession

class AuthService:
    @staticmethod
    async def authenticate(session: AsyncSession, username: str, password: str):
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user or user.hashed_password != password:
            return None
        return {"id": user.id, "username": user.username, "role": user.role}