from typing import Optional
from sqlmodel import SQLModel

class BookCreate(SQLModel):
    title: str
    author_name: str

class BookRead(SQLModel):
    id: int
    title: str
    author_name: str

class BookShort(SQLModel):
    key: str
    title: str
    author_name: str

class BookDetail(SQLModel):
    key: str
    title: str
    description: Optional[str]
    subtitle: Optional[str]
    author_name: str
