from typing import List, Optional
from sqlmodel import select
from app.books.models.book import Book
from app.books.models.book_author import BookAuthor
from app.books.models.book_subject import BookSubject
from app.database.db import AsyncSession
from app.books.models.author import Author
from sqlalchemy.orm import joinedload

class BookRepository:

    @staticmethod
    async def get_books(session: AsyncSession, title: Optional[str] = None,
                        author_name: Optional[str] = None, subject: Optional[str] = None) -> List[Book]:
        query = select(Book).options(joinedload(Book.authors))
        if author_name:
            query = query.join(BookAuthor, Book.key == BookAuthor.book_key)\
                         .join(Author, Author.key == BookAuthor.author_key)\
                         .where(Author.name.ilike(f"%{author_name}%"))
        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if subject:
            query = query.join(BookSubject, Book.key == BookSubject.book_key)\
                         .where(BookSubject.subject.ilike(f"%{subject}%"))
        query = query.distinct()
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_all_books(session: AsyncSession, title=None, author=None, subject=None) -> List[Book]:
        query = select(Book).options(joinedload(Book.authors))
        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.join(BookAuthor, Book.key == BookAuthor.book_key)\
                         .join(Author, Author.key == BookAuthor.author_key)\
                         .where(Author.name.ilike(f"%{author}%"))
        if subject:
            query = query.join(BookSubject, Book.key == BookSubject.book_key)\
                         .where(BookSubject.subject.ilike(f"%{subject}%"))
        query = query.distinct()
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_key(session: AsyncSession, key: str) -> Optional[Book]:
        query = select(Book).where(Book.key == key).options(joinedload(Book.authors))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def add_book(session: AsyncSession, book: Book) -> Book:
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book