# app/books/models/book_subject.py
from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class BookSubject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str = Field(max_length=400)
    book_key: str = Field(foreign_key="book.key")

    book: Optional["Book"] = Relationship(back_populates="subjects")