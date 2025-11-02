from sqlmodel import select
from app.books.models.author import Author
from app.database.db import AsyncSession
import secrets
from typing import List, Optional

class AuthorRepository:

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str) -> Author:
        result = await session.execute(select(Author).where(Author.name == name))
        author = result.scalar_one_or_none()
        if not author:
            author = Author(
                key=secrets.token_hex(4),
                name=name
            )
            session.add(author)
            await session.commit()
            await session.refresh(author)
        return author

    @staticmethod
    async def get_by_key(session: AsyncSession, key: str) -> Optional[Author]:
        result = await session.execute(select(Author).where(Author.key == key))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_book_id(session: AsyncSession, book_id: int) -> List[Author]:
        # Для твоей текущей модели Book, где author_key — один автор
        result = await session.execute(select(Author).where(Author.key == book_id))
        author = result.scalar_one_or_none()
        return [author] if author else []
