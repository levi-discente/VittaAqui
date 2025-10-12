from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.professional import ProfessionalProfile, ProfileTag
from app.models.user import User
from app.schemas.professional import (
    ProfessionalProfileCreate,
    ProfessionalProfileUpdate,
)


class CRUDProfessionalProfile(
    CRUDBase[ProfessionalProfile, ProfessionalProfileCreate, ProfessionalProfileUpdate]
):

    async def get_by_user_id(
        self, db: AsyncSession, *, user_id: int
    ) -> ProfessionalProfile | None:
        result = await db.execute(
            select(ProfessionalProfile)
            .where(ProfessionalProfile.user_id == user_id)
            .options(
                joinedload(ProfessionalProfile.user),
                joinedload(ProfessionalProfile.tags),
                joinedload(ProfessionalProfile.unavailable_dates),
            )
        )
        return result.unique().scalar_one_or_none()

    async def get_with_relations(
        self, db: AsyncSession, *, fk: int
    ) -> ProfessionalProfile | None:
        result = await db.execute(
            select(ProfessionalProfile)
            .where(ProfessionalProfile.id == fk)
            .options(
                joinedload(ProfessionalProfile.user),
                joinedload(ProfessionalProfile.tags),
                joinedload(ProfessionalProfile.unavailable_dates),
                joinedload(ProfessionalProfile.reviews).joinedload("patient"),
            )
        )
        return result.unique().scalar_one_or_none()

    async def get_by_identification(
        self, db: AsyncSession, *, identification: str
    ) -> ProfessionalProfile | None:
        result = await db.execute(
            select(ProfessionalProfile).where(
                ProfessionalProfile.profissional_identification == identification
            )
        )
        return result.scalar_one_or_none()

    async def list_professionals(
        self,
        db: AsyncSession,
        *,
        category: str | None = None,
        name: str | None = None,
        tags: list[str] | None = None,
        only_online: bool | None = None,
        only_presential: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ProfessionalProfile]:
        query = select(ProfessionalProfile).options(
            joinedload(ProfessionalProfile.user),
            joinedload(ProfessionalProfile.tags),
        )

        if category:
            query = query.where(ProfessionalProfile.category == category)

        if name:
            query = query.join(ProfessionalProfile.user).where(
                User.name.ilike(f"%{name}%")
            )

        if only_online is not None and only_online:
            query = query.where(ProfessionalProfile.only_online.is_(True))

        if only_presential is not None and only_presential:
            query = query.where(ProfessionalProfile.only_presential.is_(True))

        if tags:
            query = (
                query.join(ProfessionalProfile.tags)
                .where(ProfileTag.name.in_(tags))
                .distinct()
            )

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.unique().scalars().all())


professional_crud = CRUDProfessionalProfile(ProfessionalProfile)
