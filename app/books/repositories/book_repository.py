from typing import List, Optional
from sqlmodel import select
from app.books.models.book import Book
from app.books.models.author import Author
from app.database.db import AsyncSession
from sqlalchemy import join

class BookRepository:

    @staticmethod
    async def add_book(session: AsyncSession, book: Book) -> Book:
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def get_all_books(session: AsyncSession) -> List[Book]:
        result = await session.execute(select(Book))
        return result.scalars().all()
    
    @staticmethod
    async def get_by_id(session: AsyncSession, book_id: int) -> Optional[Book]:
        result = await session.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_filtered_books(session: AsyncSession, title: Optional[str] = None,
                                 author_name: Optional[str] = None) -> List[Book]:
        query = select(Book)
        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author_name:
            j = join(Book, Author, Book.author_key == Author.key)
            query = select(Book).select_from(j).where(Author.name.ilike(f"%{author_name}%"))
        result = await session.execute(query)
        return result.scalars().all()
