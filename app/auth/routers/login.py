from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from app.database.db import get_session, AsyncSession
from app.auth.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(credentials: dict, session: AsyncSession = Depends(get_session)):
    username = credentials.get("username")
    password = credentials.get("password")

    user = await AuthService.authenticate(session, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"role": user["role"], "message": "Login successful"}
