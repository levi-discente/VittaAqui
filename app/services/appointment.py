"""Appointment service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.appointment import appointment_crud
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.utils.exceptions import ConflictException, NotFoundException


async def create_appointment(
    db: AsyncSession, patient_id: int, appointment_in: AppointmentCreate
) -> Appointment:
    """Create a new appointment."""
    # Check for conflicts
    conflicts = await appointment_crud.find_conflicts(
        db,
        professional_id=appointment_in.professional_id,
        start_time=appointment_in.start_time,
        end_time=appointment_in.end_time,
    )

    if conflicts:
        raise ConflictException("Time slot already booked")

    # Check if there's a cancelled appointment we can reuse
    cancelled = await appointment_crud.find_cancelled(
        db,
        patient_id=patient_id,
        professional_id=appointment_in.professional_id,
        start_time=appointment_in.start_time,
        end_time=appointment_in.end_time,
    )

    if cancelled:
        # Reuse cancelled appointment
        cancelled.status = AppointmentStatus.PENDING
        await db.commit()
        await db.refresh(cancelled)
        return cancelled

    # Create new appointment
    appointment = Appointment(
        patient_id=patient_id,
        professional_id=appointment_in.professional_id,
        start_time=appointment_in.start_time,
        end_time=appointment_in.end_time,
        status=AppointmentStatus.PENDING,
    )
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def get_appointment(db: AsyncSession, appointment_id: int) -> Appointment:
    """Get appointment by ID."""
    appointment = await appointment_crud.get_with_relations(db, appointment_id=appointment_id)
    if not appointment:
        raise NotFoundException("Appointment not found")
    return appointment


async def get_patient_appointments(
    db: AsyncSession, patient_id: int, skip: int = 0, limit: int = 100
) -> list[AppointmentResponse]:
    """Get all appointments for a patient."""
    appointments = await appointment_crud.get_by_patient(
        db, patient_id=patient_id, skip=skip, limit=limit
    )

    return [
        AppointmentResponse(
            id=apt.id,
            patient_id=apt.patient_id,
            patient_name=apt.patient.name if apt.patient else None,
            professional_id=apt.professional_id,
            professional_name=apt.professional.user.name if apt.professional and apt.professional.user else None,
            start_time=apt.start_time,
            end_time=apt.end_time,
            status=apt.status,
            created_at=apt.created_at,
            updated_at=apt.updated_at,
        )
        for apt in appointments
    ]


async def get_professional_appointments(
    db: AsyncSession, professional_id: int, skip: int = 0, limit: int = 100
) -> list[AppointmentResponse]:
    """Get all appointments for a professional."""
    appointments = await appointment_crud.get_by_professional(
        db, professional_id=professional_id, skip=skip, limit=limit
    )

    return [
        AppointmentResponse(
            id=apt.id,
            patient_id=apt.patient_id,
            patient_name=apt.patient.name if apt.patient else None,
            professional_id=apt.professional_id,
            professional_name=None,
            start_time=apt.start_time,
            end_time=apt.end_time,
            status=apt.status,
            created_at=apt.created_at,
            updated_at=apt.updated_at,
        )
        for apt in appointments
    ]


async def update_appointment(
    db: AsyncSession, appointment_id: int, appointment_in: AppointmentUpdate
) -> Appointment:
    """Update an appointment."""
    appointment = await get_appointment(db, appointment_id)

    # If changing time, check for conflicts
    if appointment_in.start_time or appointment_in.end_time:
        start_time = appointment_in.start_time or appointment.start_time
        end_time = appointment_in.end_time or appointment.end_time

        conflicts = await appointment_crud.find_conflicts(
            db,
            professional_id=appointment.professional_id,
            start_time=start_time,
            end_time=end_time,
            exclude_id=appointment.id,
        )

        if conflicts:
            raise ConflictException("Time slot already booked")

    # Update appointment
    updated = await appointment_crud.update(db, db_obj=appointment, obj_in=appointment_in)
    await db.commit()
    await db.refresh(updated)
    return updated


async def delete_appointment(db: AsyncSession, appointment_id: int) -> None:
    """Delete an appointment."""
    appointment = await get_appointment(db, appointment_id)
    await appointment_crud.delete(db, id=appointment.id)
    await db.commit()
