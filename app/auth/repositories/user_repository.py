from sqlmodel import select
from app.auth.models import User

class UserRepository:
    @staticmethod
    async def get_by_username(session, username: str):
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()