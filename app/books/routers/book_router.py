# app/books/routers/book_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.database.db import get_session
from app.books.schemas.book import BookShort, BookDetail, BookCreate
from app.books.schemas.author import AuthorDetail
from app.books.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookShort)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, book)

@router.get("/", response_model=List[BookShort])
async def get_books(
    session: AsyncSession = Depends(get_session),
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
):
    return await BookService.get_all_books(session, title, author, subject)

@router.get("/{book_key}", response_model=BookDetail)
async def get_book(book_key: str, session: AsyncSession = Depends(get_session)):
    book = await BookService.get_book_by_key(session, book_key)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_key}/authors", response_model=List[AuthorDetail])
async def get_book_authors(book_key: str, session: AsyncSession = Depends(get_session)):
    return await BookService.get_book_authors_details(session, book_key)