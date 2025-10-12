from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models.enums import Role
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)
from app.services import appointment as appointment_service
from app.services import professional as professional_service
from app.utils.exceptions import ForbiddenException

router = APIRouter()


@router.post("/", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    appointment_in: AppointmentCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.role != Role.PATIENT:
        raise ForbiddenException("Only patients can create appointments")

    appointment = await appointment_service.create_appointment(
        db, current_user.id, appointment_in
    )

    return AppointmentResponse(
        id=appointment.id,
        patient_id=appointment.patient_id,
        patient_name=current_user.name,
        professional_id=appointment.professional_id,
        professional_name=None,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        status=appointment.status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
    )


@router.get("/my-appointments", response_model=list[AppointmentResponse])
@router.get("/my", response_model=list[AppointmentResponse])
async def get_my_appointments(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    if current_user.role == Role.PATIENT:
        return await appointment_service.get_patient_appointments(
            db, current_user.id, skip=skip, limit=limit
        )

    profile = await professional_service.get_professional_profile_by_user(
        db, current_user.id
    )
    return await appointment_service.get_professional_appointments(
        db, profile.id, skip=skip, limit=limit
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    appointment = await appointment_service.get_appointment(db, appointment_id)

    if current_user.role == Role.PATIENT:
        if appointment.patient_id != current_user.id:
            raise ForbiddenException("Not authorized to view this appointment")
    else:
        profile = await professional_service.get_professional_profile_by_user(
            db, current_user.id
        )
        if appointment.professional_id != profile.id:
            raise ForbiddenException("Not authorized to view this appointment")

    return AppointmentResponse(
        id=appointment.id,
        patient_id=appointment.patient_id,
        patient_name=appointment.patient.name if appointment.patient else None,
        professional_id=appointment.professional_id,
        professional_name=(
            appointment.professional.user.name
            if appointment.professional and appointment.professional.user
            else None
        ),
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        status=appointment.status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
    )


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    appointment = await appointment_service.get_appointment(db, appointment_id)

    if current_user.role == Role.PATIENT:
        if appointment.patient_id != current_user.id:
            raise ForbiddenException("Not authorized to update this appointment")
    else:
        profile = await professional_service.get_professional_profile_by_user(
            db, current_user.id
        )
        if appointment.professional_id != profile.id:
            raise ForbiddenException("Not authorized to update this appointment")

    updated = await appointment_service.update_appointment(
        db, appointment_id, appointment_in
    )

    return AppointmentResponse(
        id=updated.id,
        patient_id=updated.patient_id,
        patient_name=updated.patient.name if updated.patient else None,
        professional_id=updated.professional_id,
        professional_name=(
            updated.professional.user.name
            if updated.professional and updated.professional.user
            else None
        ),
        start_time=updated.start_time,
        end_time=updated.end_time,
        status=updated.status,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


@router.delete("/{appointment_id}", status_code=204)
async def delete_appointment(
    appointment_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    appointment = await appointment_service.get_appointment(db, appointment_id)

    if current_user.role == Role.PATIENT:
        if appointment.patient_id != current_user.id:
            raise ForbiddenException("Not authorized to delete this appointment")
    else:
        profile = await professional_service.get_professional_profile_by_user(
            db, current_user.id
        )
        if appointment.professional_id != profile.id:
            raise ForbiddenException("Not authorized to delete this appointment")

    await appointment_service.delete_appointment(db, appointment_id)
