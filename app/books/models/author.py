from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.books.models.book import Book
    from app.books.models.book_author import BookAuthor

class Author(SQLModel, table=True):
    key: str = Field(primary_key=True, max_length=128)
    name: str = Field(max_length=500)
    bio: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    wikipedia: Optional[str] = None

    # Убираем link_model - SQLModel найдёт его сам через имя таблицы
    books: List["Book"] = Relationship(back_populates="authors")