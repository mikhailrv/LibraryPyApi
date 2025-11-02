from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.database.db import get_session
from app.books.schemas.book import BookShort, BookDetail
from app.books.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookShort])
async def get_books(
    title: Optional[str] = None,
    author_name: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    return await BookService.get_books(session, title, author_name)

@router.get("/{book_id}", response_model=BookDetail)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await BookService.get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_id}/authors")
async def get_book_authors(book_id: int, session: AsyncSession = Depends(get_session)):
    return await BookService.get_authors_by_book_id(session, book_id)
