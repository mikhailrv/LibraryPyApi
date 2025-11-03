from typing import Optional, List
from sqlmodel import SQLModel

class BookCreate(SQLModel):
    title: str
    author_name: str

class BookShort(SQLModel):
    key: str
    title: str
    author_name: str

class BookDetail(SQLModel):
    key: str
    title: str
    subtitle: Optional[str] = None
    first_publish_date: Optional[str] = None
    description: Optional[str] = None
    authors: Optional[List[str]] = None