# app/books/services/book_service.py
from typing import List, Optional
from app.books.models.book import Book
from app.books.models.book_author import BookAuthor
from app.books.repositories.book_repository import BookRepository
from app.books.repositories.author_repository import AuthorRepository
from app.books.schemas.author import AuthorDetail
from app.books.schemas.book import BookCreate, BookShort, BookDetail
from app.database.db import AsyncSession
import secrets

class BookService:

    @staticmethod
    async def add_book(session: AsyncSession, book_create: BookCreate) -> BookShort:
        author = await AuthorRepository.get_or_create(session, book_create.author_name)

        book = Book(
            key=secrets.token_hex(8),
            title=book_create.title,
        )
        saved = await BookRepository.add_book(session, book)

        # связь многие-ко-многим
        session.add(BookAuthor(book_key=saved.key, author_key=author.key))
        await session.commit()

        return BookShort(key=saved.key, title=saved.title, author_name=author.name)

    @staticmethod
    async def get_all_books(session: AsyncSession, title=None, author=None, subject=None) -> List[BookShort]:
        books = await BookRepository.get_all_books(session, title, author, subject)
        return [
            BookShort(
                key=b.key,
                title=b.title,
                author_name=", ".join(a.name for a in b.authors)
            ) for b in books
        ]

    @staticmethod
    async def get_book_by_key(session: AsyncSession, key: str) -> Optional[BookDetail]:
        book = await BookRepository.get_by_key(session, key)
        if not book:
            return None
        return BookDetail(
            key=book.key,
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            authors=[a.name for a in book.authors]
        )

    @staticmethod
    async def get_book_authors_details(session: AsyncSession, book_key: str) -> List[AuthorDetail]:
        authors = await AuthorRepository.get_authors(session, book_key)
        return [
            AuthorDetail(
                key=a.key,
                name=a.name,
                bio=a.bio,
                birth_date=a.birth_date,
                death_date=a.death_date,
                wikipedia=a.wikipedia,
            ) for a in authors
        ]