
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.models.enums import Role
from app.models.professional import ProfessionalProfile
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import hash_password
from app.utils.exceptions import BadRequestException, NotFoundException


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    existing_user = await user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise BadRequestException("Email already registered")

    existing_cpf = await user_crud.get_by_cpf(db, cpf=user_in.cpf)
    if existing_cpf:
        raise BadRequestException("CPF already registered")

    hashed_password = hash_password(user_in.password)

    user = await user_crud.create_user(db, obj_in=user_in, hashed_password=hashed_password)

    if user_in.role == Role.PROFESSIONAL:
        if not user_in.profissional_identification or not user_in.category:
            raise BadRequestException(
                "Professional identification and category are required for professionals"
            )

        # Criar perfil profissional com valores padrão
        profile = ProfessionalProfile(
            user_id=user.id,
            profissional_identification=user_in.profissional_identification,
            category=user_in.category,
            bio="Profissional de saúde",
            services="",
            price=0.0,
            only_online=False,
            only_presential=False,
            rating=0.0,
            num_reviews=0,
            available_days_of_week="",
            start_hour="",
            end_hour="",
        )
        db.add(profile)

    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise NotFoundException("User not found")
    return user


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
    user = await get_user(db, user_id)

    if user_in.email and user_in.email != user.email:
        existing = await user_crud.get_by_email(db, email=user_in.email)
        if existing:
            raise BadRequestException("Email already in use")

    updated_user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    await db.commit()
    await db.refresh(updated_user)
    return updated_user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    user = await get_user(db, user_id)
    await user_crud.delete(db, id=user.id)
    await db.commit()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    return await user_crud.get_multi(db, skip=skip, limit=limit)
