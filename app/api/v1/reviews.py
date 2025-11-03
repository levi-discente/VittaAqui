
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.crud.review import review as review_crud
from app.models.enums import Role
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)
from app.services.review import review_service
from app.utils.exceptions import ForbiddenException

router = APIRouter()


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a review",
)
async def create_review(
    review_in: ReviewCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    """
    Create a review for a completed appointment.

    **Requirements:**
    - Only patients can create reviews
    - Appointment must be completed
    - Patient must own the appointment
    - Only one review per appointment
    """
    if current_user.role != Role.PATIENT:
        raise ForbiddenException("Only patients can create reviews")

    review = await review_service.create_review(
        db, review_in=review_in, patient_id=current_user.id
    )

    return ReviewResponse.model_validate(review)


@router.get(
    "/my",
    response_model=list[ReviewResponse],
    summary="Get my reviews",
)
async def get_my_reviews(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[ReviewResponse]:
    """
    Get all reviews created by the current patient.
    """
    if current_user.role != Role.PATIENT:
        raise ForbiddenException("Only patients can view their reviews")

    reviews = await review_service.get_patient_reviews(
        db, patient_id=current_user.id, skip=skip, limit=limit
    )

    return [ReviewResponse.model_validate(review) for review in reviews]


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Get review by ID",
)
async def get_review(
    review_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    """
    Get a specific review by ID.
    """
    review = await review_crud.get_with_patient(db, review_id=review_id)
    if not review:
        from app.utils.exceptions import NotFoundException

        raise NotFoundException("Review not found")

    return ReviewResponse.model_validate(review)


@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Update a review",
)
async def update_review(
    review_id: int,
    review_in: ReviewUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    """
    Update a review. Only the patient who created it can update.
    """
    if current_user.role != Role.PATIENT:
        raise ForbiddenException("Only patients can update reviews")

    review = await review_service.update_review(
        db, review_id=review_id, review_in=review_in, patient_id=current_user.id
    )

    return ReviewResponse.model_validate(review)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a review",
)
async def delete_review(
    review_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """
    Delete a review. Only the patient who created it can delete.
    """
    if current_user.role != Role.PATIENT:
        raise ForbiddenException("Only patients can delete reviews")

    await review_service.delete_review(
        db, review_id=review_id, patient_id=current_user.id
    )


@router.get(
    "/appointment/{appointment_id}",
    response_model=ReviewResponse | None,
    summary="Get review for an appointment",
)
async def get_appointment_review(
    appointment_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse | None:
    """
    Get the review for a specific appointment (if exists).
    """
    review = await review_service.get_appointment_review(
        db, appointment_id=appointment_id
    )

    if not review:
        return None

    return ReviewResponse.model_validate(review)
