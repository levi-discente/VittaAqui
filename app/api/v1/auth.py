from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.enums import Role
from app.schemas.auth import LoginResponse
from app.schemas.user import UserCreate, UserResponse
from app.services import auth as auth_service
from app.services import user as user_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    cpf: Annotated[str, Form()],
    role: Annotated[str, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],
    phone: Annotated[str | None, Form()] = None,
    cep: Annotated[str | None, Form()] = None,
    uf: Annotated[str | None, Form()] = None,
    city: Annotated[str | None, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    profissional_identification: Annotated[str | None, Form()] = None,
    category: Annotated[str | None, Form()] = None,
    profile_image_url: Annotated[str | None, Form()] = None,
):
    user_in = UserCreate(
        name=name,
        email=email,
        password=password,
        cpf=cpf,
        role=Role(role),
        phone=phone,
        cep=cep,
        uf=uf,
        city=city,
        address=address,
        profissional_identification=profissional_identification,
        category=category,
        profile_image_url=profile_image_url,
    )
    user = await user_service.create_user(db, user_in)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=LoginResponse)
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await auth_service.login(db, email, password)
