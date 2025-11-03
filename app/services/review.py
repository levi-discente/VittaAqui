
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.professional import professional_crud
from app.crud.review import review as review_crud
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.utils.exceptions import BadRequestException, NotFoundException


class ReviewService:

    async def create_review(
        self,
        db: AsyncSession,
        *,
        review_in: ReviewCreate,
        patient_id: int,
    ) -> Review:
        """
        Create a review for a completed appointment.
        Validates that:
        - Appointment exists and is completed
        - Patient owns the appointment
        - Review doesn't already exist for this appointment
        """
        # Get appointment
        appointment = await db.get(Appointment, review_in.appointment_id)
        if not appointment:
            raise NotFoundException("Appointment not found")

        # Validate appointment is completed
        if appointment.status != AppointmentStatus.COMPLETED:
            raise BadRequestException(
                "Can only review completed appointments"
            )

        # Validate patient owns the appointment
        if appointment.patient_id != patient_id:
            raise BadRequestException(
                "You can only review your own appointments"
            )

        # Check if review already exists
        existing_review = await review_crud.get_by_appointment(
            db, appointment_id=review_in.appointment_id
        )
        if existing_review:
            raise BadRequestException(
                "Review already exists for this appointment"
            )

        # Create review
        review_data = review_in.model_dump()
        review_data["patient_id"] = patient_id
        review_data["professional_id"] = appointment.professional_id

        new_review = Review(**review_data)
        db.add(new_review)
        await db.flush()
        await db.refresh(new_review)

        # Update professional rating
        await self.update_professional_rating(
            db, professional_id=appointment.professional_id
        )

        await db.commit()
        await db.refresh(new_review)

        return new_review

    async def update_review(
        self,
        db: AsyncSession,
        *,
        review_id: int,
        review_in: ReviewUpdate,
        patient_id: int,
    ) -> Review:
        """
        Update a review. Only the patient who created it can update.
        """
        # Get review
        db_review = await review_crud.get(db, pk=review_id)
        if not db_review:
            raise NotFoundException("Review not found")

        # Validate ownership
        if db_review.patient_id != patient_id:
            raise BadRequestException("You can only update your own reviews")

        # Update review
        updated_review = await review_crud.update(
            db, db_obj=db_review, obj_in=review_in
        )

        # Recalculate professional rating if rating changed
        if review_in.rating is not None:
            await self.update_professional_rating(
                db, professional_id=db_review.professional_id
            )

        await db.commit()
        await db.refresh(updated_review)

        return updated_review

    async def delete_review(
        self,
        db: AsyncSession,
        *,
        review_id: int,
        patient_id: int,
    ) -> None:
        """
        Delete a review. Only the patient who created it can delete.
        """
        # Get review
        db_review = await review_crud.get(db, pk=review_id)
        if not db_review:
            raise NotFoundException("Review not found")

        # Validate ownership
        if db_review.patient_id != patient_id:
            raise BadRequestException("You can only delete your own reviews")

        professional_id = db_review.professional_id

        # Delete review
        await review_crud.delete(db, pk=review_id)

        # Recalculate professional rating
        await self.update_professional_rating(db, professional_id=professional_id)

        await db.commit()

    async def update_professional_rating(
        self,
        db: AsyncSession,
        *,
        professional_id: int,
    ) -> None:
        """
        Recalculate and update professional's average rating and review count.
        """
        stats = await review_crud.get_stats_by_professional(
            db, professional_id=professional_id
        )

        professional = await professional_crud.get(db, pk=professional_id)
        if professional:
            professional.rating = stats["average_rating"]
            professional.num_reviews = stats["total_reviews"]
            db.add(professional)
            await db.flush()

    async def get_professional_reviews(
        self,
        db: AsyncSession,
        *,
        professional_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Review], int]:
        """
        Get all reviews for a professional with pagination.
        Returns (reviews, total_count)
        """
        reviews = await review_crud.get_by_professional(
            db, professional_id=professional_id, skip=skip, limit=limit
        )
        total = await review_crud.count_by_professional(
            db, professional_id=professional_id
        )
        return reviews, total

    async def get_professional_stats(
        self,
        db: AsyncSession,
        *,
        professional_id: int,
    ) -> dict:
        """
        Get review statistics for a professional.
        """
        return await review_crud.get_stats_by_professional(
            db, professional_id=professional_id
        )

    async def get_patient_reviews(
        self,
        db: AsyncSession,
        *,
        patient_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Review]:
        """
        Get all reviews created by a patient.
        """
        return await review_crud.get_by_patient(
            db, patient_id=patient_id, skip=skip, limit=limit
        )

    async def get_appointment_review(
        self,
        db: AsyncSession,
        *,
        appointment_id: int,
    ) -> Review | None:
        """
        Get review for a specific appointment.
        """
        return await review_crud.get_by_appointment(db, appointment_id=appointment_id)


review_service = ReviewService()
