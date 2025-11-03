
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):

    async def get_by_appointment(
        self, db: AsyncSession, *, appointment_id: int
    ) -> Review | None:
        result = await db.execute(
            select(Review)
            .where(Review.appointment_id == appointment_id)
            .options(joinedload(Review.patient))
        )
        return result.scalar_one_or_none()

    async def get_by_professional(
        self,
        db: AsyncSession,
        *,
        professional_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Review]:
        result = await db.execute(
            select(Review)
            .where(Review.professional_id == professional_id)
            .options(joinedload(Review.patient))
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.unique().scalars().all())

    async def count_by_professional(
        self, db: AsyncSession, *, professional_id: int
    ) -> int:
        result = await db.execute(
            select(func.count(Review.id)).where(
                Review.professional_id == professional_id
            )
        )
        return result.scalar_one()

    async def get_by_patient(
        self,
        db: AsyncSession,
        *,
        patient_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Review]:
        result = await db.execute(
            select(Review)
            .where(Review.patient_id == patient_id)
            .options(joinedload(Review.professional))
            .order_by(Review.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.unique().scalars().all())

    async def get_stats_by_professional(
        self, db: AsyncSession, *, professional_id: int
    ) -> dict:
        # Get average rating and total reviews
        result = await db.execute(
            select(
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("total_reviews"),
            ).where(Review.professional_id == professional_id)
        )
        stats = result.one()

        # Get distribution of ratings
        distribution_result = await db.execute(
            select(Review.rating, func.count(Review.id))
            .where(Review.professional_id == professional_id)
            .group_by(Review.rating)
        )
        distribution = {str(int(row[0])): row[1] for row in distribution_result.all()}

        # Ensure all ratings (1-5) are present
        for i in range(1, 6):
            if str(i) not in distribution:
                distribution[str(i)] = 0

        return {
            "average_rating": round(float(stats.average_rating or 0), 1),
            "total_reviews": stats.total_reviews or 0,
            "distribution": dict(sorted(distribution.items(), reverse=True)),
        }

    async def get_with_patient(
        self, db: AsyncSession, *, review_id: int
    ) -> Review | None:
        result = await db.execute(
            select(Review)
            .where(Review.id == review_id)
            .options(joinedload(Review.patient))
        )
        return result.scalar_one_or_none()


review = CRUDReview(Review)
