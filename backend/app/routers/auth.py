from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserCreate, Token
from app.crud import create_user, authenticate_user, update_password
from app.core.security import create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.email, user.password)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await create_user(db, user.email, user.password)
    return {"msg": "User registered successfully"}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout():
    return {"msg": "Logged out"}


@router.post("/reset-password")
async def reset_password(user: UserCreate, db: AsyncSession = Depends(get_db)):
    updated = await update_password(db, user.email, user.password)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"msg": "Password reset successful"}
