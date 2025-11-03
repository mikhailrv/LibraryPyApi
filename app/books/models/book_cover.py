# app/books/models/book_cover.py
from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class BookCover(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cover_file: int
    book_key: str = Field(foreign_key="book.key")

    book: Optional["Book"] = Relationship(back_populates="covers")