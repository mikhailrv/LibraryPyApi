from typing import Optional
from sqlmodel import SQLModel

class AuthorDetail(SQLModel):
    key: str
    name: str
    bio: Optional[str]
    birth_date: Optional[str]
    death_date: Optional[str]
    wikipedia: Optional[str]