
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models.enums import Role
from app.schemas.appointment import AppointmentResponse
from app.schemas.professional import (
    AvailableSlotsResponse,
    ProfessionalProfileCreate,
    ProfessionalProfileResponse,
    ProfessionalProfileUpdate,
)
from app.services import appointment as appointment_service
from app.services import professional as professional_service
from app.utils.exceptions import ForbiddenException

router = APIRouter()


@router.post("/", response_model=ProfessionalProfileResponse, status_code=201)
async def create_professional_profile(
    profile_in: ProfessionalProfileCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role != Role.PROFESSIONAL:
        raise ForbiddenException("Only professionals can create a profile")

    profile = await professional_service.create_full_professional_profile(
        db, current_user.id, profile_in
    )

    return ProfessionalProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        category=profile.category,
        profissional_identification=profile.profissional_identification,
        services=profile.services,
        price=profile.price,
        only_online=profile.only_online,
        only_presential=profile.only_presential,
        rating=profile.rating,
        num_reviews=profile.num_reviews,
        available_days_of_week=profile.available_days_of_week,
        start_hour=profile.start_hour,
        end_hour=profile.end_hour,
        user_name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        cep=current_user.cep,
        uf=current_user.uf,
        city=current_user.city,
        address=current_user.address,
        tags=[],
        unavailable_dates=[],
    )


@router.get("/me", response_model=ProfessionalProfileResponse)
async def get_my_professional_profile(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role != Role.PROFESSIONAL:
        raise ForbiddenException("Only professionals have profiles")

    profile = await professional_service.get_professional_profile_by_user(db, current_user.id)

    return ProfessionalProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        category=profile.category,
        profissional_identification=profile.profissional_identification,
        services=profile.services,
        price=profile.price,
        only_online=profile.only_online,
        only_presential=profile.only_presential,
        rating=profile.rating,
        num_reviews=profile.num_reviews,
        available_days_of_week=profile.available_days_of_week,
        start_hour=profile.start_hour,
        end_hour=profile.end_hour,
        user_name=profile.user.name if profile.user else None,
        email=profile.user.email if profile.user else None,
        phone=profile.user.phone if profile.user else None,
        cep=profile.user.cep if profile.user else None,
        uf=profile.user.uf if profile.user else None,
        city=profile.user.city if profile.user else None,
        address=profile.user.address if profile.user else None,
        tags=[tag.name for tag in profile.tags],
        unavailable_dates=[],
    )


@router.put("/me", response_model=ProfessionalProfileResponse)
async def update_my_professional_profile(
    profile_in: ProfessionalProfileUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role != Role.PROFESSIONAL:
        raise ForbiddenException("Only professionals have profiles")

    profile = await professional_service.get_professional_profile_by_user(db, current_user.id)
    updated_profile = await professional_service.update_professional_profile(
        db, current_user.id, profile.id, profile_in
    )

    return ProfessionalProfileResponse(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        bio=updated_profile.bio,
        category=updated_profile.category,
        profissional_identification=updated_profile.profissional_identification,
        services=updated_profile.services,
        price=updated_profile.price,
        only_online=updated_profile.only_online,
        only_presential=updated_profile.only_presential,
        rating=updated_profile.rating,
        num_reviews=updated_profile.num_reviews,
        available_days_of_week=updated_profile.available_days_of_week,
        start_hour=updated_profile.start_hour,
        end_hour=updated_profile.end_hour,
        user_name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        cep=current_user.cep,
        uf=current_user.uf,
        city=current_user.city,
        address=current_user.address,
        tags=[],
        unavailable_dates=[],
    )


@router.get("/", response_model=list[ProfessionalProfileResponse])
async def list_professionals(
    db: Annotated[AsyncSession, Depends(get_db)],
    category: Annotated[str | None, Query()] = None,
    name: Annotated[str | None, Query()] = None,
    tags: Annotated[list[str] | None, Query()] = None,
    only_online: Annotated[bool | None, Query()] = None,
    only_presential: Annotated[bool | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    # Converter strings vazias em None
    category = category if category and category.strip() else None
    name = name if name and name.strip() else None
    tags = [t for t in (tags or []) if t and t.strip()] or None
    
    return await professional_service.list_professionals(
        db,
        category=category,
        name=name,
        tags=tags,
        only_online=only_online,
        only_presential=only_presential,
        skip=skip,
        limit=limit,
    )


@router.get("/user/{user_id}", response_model=ProfessionalProfileResponse)
async def get_professional_profile_by_user_id(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    profile = await professional_service.get_professional_profile_by_user(db, user_id)

    return ProfessionalProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        category=profile.category,
        profissional_identification=profile.profissional_identification,
        services=profile.services,
        price=profile.price,
        only_online=profile.only_online,
        only_presential=profile.only_presential,
        rating=profile.rating,
        num_reviews=profile.num_reviews,
        available_days_of_week=profile.available_days_of_week,
        start_hour=profile.start_hour,
        end_hour=profile.end_hour,
        user_name=profile.user.name if profile.user else None,
        email=profile.user.email if profile.user else None,
        phone=profile.user.phone if profile.user else None,
        cep=profile.user.cep if profile.user else None,
        uf=profile.user.uf if profile.user else None,
        city=profile.user.city if profile.user else None,
        address=profile.user.address if profile.user else None,
        tags=[tag.name for tag in profile.tags],
        unavailable_dates=[],
    )


@router.get("/{profile_id}", response_model=ProfessionalProfileResponse)
async def get_professional_profile(
    profile_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    profile = await professional_service.get_professional_profile(db, profile_id)

    return ProfessionalProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        category=profile.category,
        profissional_identification=profile.profissional_identification,
        services=profile.services,
        price=profile.price,
        only_online=profile.only_online,
        only_presential=profile.only_presential,
        rating=profile.rating,
        num_reviews=profile.num_reviews,
        available_days_of_week=profile.available_days_of_week,
        start_hour=profile.start_hour,
        end_hour=profile.end_hour,
        user_name=profile.user.name if profile.user else None,
        email=profile.user.email if profile.user else None,
        phone=profile.user.phone if profile.user else None,
        cep=profile.user.cep if profile.user else None,
        uf=profile.user.uf if profile.user else None,
        city=profile.user.city if profile.user else None,
        address=profile.user.address if profile.user else None,
        tags=[tag.name for tag in profile.tags],
        unavailable_dates=[],
    )


@router.put("/{profile_id}", response_model=ProfessionalProfileResponse)
async def update_professional_profile(
    profile_id: int,
    profile_in: ProfessionalProfileUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    updated_profile = await professional_service.update_professional_profile(
        db, current_user.id, profile_id, profile_in
    )

    return ProfessionalProfileResponse(
        id=updated_profile.id,
        user_id=updated_profile.user_id,
        bio=updated_profile.bio,
        category=updated_profile.category,
        profissional_identification=updated_profile.profissional_identification,
        services=updated_profile.services,
        price=updated_profile.price,
        only_online=updated_profile.only_online,
        only_presential=updated_profile.only_presential,
        rating=updated_profile.rating,
        num_reviews=updated_profile.num_reviews,
        available_days_of_week=updated_profile.available_days_of_week,
        start_hour=updated_profile.start_hour,
        end_hour=updated_profile.end_hour,
        user_name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        cep=current_user.cep,
        uf=current_user.uf,
        city=current_user.city,
        address=current_user.address,
        tags=[],
        unavailable_dates=[],
    )


@router.delete("/{profile_id}", status_code=204)
async def delete_professional_profile(
    profile_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await professional_service.delete_professional_profile(db, current_user.id, profile_id)


@router.get("/{profile_id}/appointments", response_model=list[AppointmentResponse])
async def get_professional_appointments(
    profile_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """Listar agendamentos de um profissional específico."""
    return await appointment_service.get_professional_appointments_by_date(
        db, profile_id, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )


@router.get("/{profile_id}/available-slots", response_model=AvailableSlotsResponse)
async def get_available_slots(
    profile_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    target_date: Annotated[date, Query()],
    duration_minutes: Annotated[int, Query(ge=15, le=480)] = 60,
):
    """Calcular horários disponíveis de um profissional para uma data específica."""
    return await professional_service.get_available_slots(
        db, profile_id, target_date, duration_minutes
    )
