"""User service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.models.enums import Role
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import hash_password
from app.services.professional import create_professional_profile
from app.utils.exceptions import BadRequestException, NotFoundException


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Create a new user."""
    # Check if email already exists
    existing_user = await user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise BadRequestException("Email already registered")

    # Check if CPF already exists
    existing_cpf = await user_crud.get_by_cpf(db, cpf=user_in.cpf)
    if existing_cpf:
        raise BadRequestException("CPF already registered")

    # Hash password
    hashed_password = hash_password(user_in.password)

    # Create user
    user = await user_crud.create_user(db, obj_in=user_in, hashed_password=hashed_password)

    # If professional, create profile
    if user_in.role == Role.PROFESSIONAL:
        if not user_in.profissional_identification or not user_in.category:
            raise BadRequestException(
                "Professional identification and category are required for professionals"
            )

        await create_professional_profile(
            db,
            user_id=user.id,
            profissional_identification=user_in.profissional_identification,
            category=user_in.category,
        )

    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    """Get user by ID."""
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise NotFoundException("User not found")
    return user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
    """Update user information."""
    user = await get_user(db, user_id)

    # Check email uniqueness if changing
    if user_in.email and user_in.email != user.email:
        existing = await user_crud.get_by_email(db, email=user_in.email)
        if existing:
            raise BadRequestException("Email already in use")

    updated_user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    await db.commit()
    await db.refresh(updated_user)
    return updated_user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """Delete user."""
    user = await get_user(db, user_id)
    await user_crud.delete(db, id=user.id)
    await db.commit()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination."""
    return await user_crud.get_multi(db, skip=skip, limit=limit)
