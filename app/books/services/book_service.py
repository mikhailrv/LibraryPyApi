from typing import List, Optional
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.repositories.author_repository import AuthorRepository
from app.books.schemas.book import BookCreate
from app.database.db import AsyncSession
import secrets

class BookService:

    @staticmethod
    async def add_book(session: AsyncSession, book_create: BookCreate) -> Book:
        author = await AuthorRepository.get_or_create(session, book_create.author_name)
        book = Book(
            key=secrets.token_hex(4), 
            title=book_create.title,
            author_key=author.key
        )
        return await BookRepository.add_book(session, book)

    @staticmethod
    async def get_books(session: AsyncSession, title=None, author_name=None) -> List[Book]:
        return await BookRepository.get_filtered_books(session, title, author_name)

    @staticmethod
    async def get_book_by_id(session: AsyncSession, book_id: int) -> Optional[Book]:
        return await BookRepository.get_by_id(session, book_id)

    @staticmethod
    async def get_authors_by_book_id(session: AsyncSession, book_id: int) -> List:
        book = await BookRepository.get_by_id(session, book_id)
        if not book:
            return []
        author = await AuthorRepository.get_by_key(session, book.author_key)
        return [author] if author else []
