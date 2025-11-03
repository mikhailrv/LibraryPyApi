from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.books.models.author import Author
    from app.books.models.book_cover import BookCover
    from app.books.models.book_subject import BookSubject

class Book(SQLModel, table=True):
    key: str = Field(primary_key=True, max_length=128)
    title: str = Field(max_length=500)
    subtitle: Optional[str] = None
    first_publish_date: Optional[str] = None
    description: Optional[str] = None

    authors: List["Author"] = Relationship(back_populates="books")
    subjects: List["BookSubject"] = Relationship(back_populates="book")
    covers: List["BookCover"] = Relationship(back_populates="book")