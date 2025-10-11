
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_cpf(self, db: AsyncSession, *, cpf: str) -> User | None:
        result = await db.execute(select(User).where(User.cpf == cpf))
        return result.scalar_one_or_none()

    async def create_user(self, db: AsyncSession, *, obj_in: UserCreate, hashed_password: str) -> User:
        obj_data = obj_in.model_dump(exclude={"password", "profissional_identification", "category"})
        db_obj = User(**obj_data, password=hashed_password)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)
