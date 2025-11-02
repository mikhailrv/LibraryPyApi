from app.auth.models.user import User
from sqlmodel import select
from app.database.db import AsyncSession

class AuthService:

    @staticmethod
    async def authenticate(session: AsyncSession, username: str, password: str):
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return None
        # для примера используем plain text (позже заменим на bcrypt)
        if user.password_hash != password:
            return None
        return {"id": user.id, "username": user.username, "role": user.role}
