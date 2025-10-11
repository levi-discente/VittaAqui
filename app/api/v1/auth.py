
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginResponse
from app.schemas.user import UserCreate, UserResponse
from app.services import auth as auth_service
from app.services import user as user_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_in: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await user_service.create_user(db, user_in)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=LoginResponse)
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await auth_service.login(db, email, password)
