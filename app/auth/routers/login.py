# app/auth/routers/login.py
from fastapi import APIRouter, Depends, HTTPException
from app.auth.schemas import LoginRequest, LoginResponse
from app.database.db import get_session, AsyncSession
from app.auth.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    result = await AuthService.authenticate(session, data.username, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return LoginResponse(role=result["role"], message="Login successful")