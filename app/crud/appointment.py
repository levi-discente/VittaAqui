
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.appointment import Appointment
from app.models.enums import AppointmentStatus
from app.models.professional import ProfessionalProfile
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class CRUDAppointment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):

    async def get_with_relations(
        self, db: AsyncSession, *, appointment_id: int
    ) -> Appointment | None:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.id == appointment_id)
            .options(
                joinedload(Appointment.patient),
                joinedload(Appointment.professional).joinedload(
                    ProfessionalProfile.user
                ),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_patient(
        self, db: AsyncSession, *, patient_id: int, skip: int = 0, limit: int = 100
    ) -> list[Appointment]:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .options(
                joinedload(Appointment.professional).joinedload(
                    ProfessionalProfile.user
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_professional(
        self, db: AsyncSession, *, professional_id: int, skip: int = 0, limit: int = 100
    ) -> list[Appointment]:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.professional_id == professional_id)
            .options(joinedload(Appointment.patient))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def find_conflicts(
        self,
        db: AsyncSession,
        *,
        professional_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_id: int | None = None,
    ) -> list[Appointment]:
        query = select(Appointment).where(
            Appointment.professional_id == professional_id,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
            Appointment.status != AppointmentStatus.CANCELLED,
        )

        if exclude_id:
            query = query.where(Appointment.id != exclude_id)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def find_cancelled(
        self,
        db: AsyncSession,
        *,
        patient_id: int,
        professional_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> Appointment | None:
        result = await db.execute(
            select(Appointment).where(
                Appointment.patient_id == patient_id,
                Appointment.professional_id == professional_id,
                Appointment.start_time == start_time,
                Appointment.end_time == end_time,
                Appointment.status == AppointmentStatus.CANCELLED,
            )
        )
        return result.scalar_one_or_none()


appointment_crud = CRUDAppointment(Appointment)
