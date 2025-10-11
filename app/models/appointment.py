
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AppointmentStatus

if TYPE_CHECKING:
    from app.models.professional import ProfessionalProfile
    from app.models.user import User


class Appointment(Base):

    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professional_profiles.id"), index=True
    )

    start_time: Mapped[datetime] = mapped_column(index=True)
    end_time: Mapped[datetime] = mapped_column()
    status: Mapped[AppointmentStatus] = mapped_column(
        String(20), default=AppointmentStatus.PENDING
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    patient: Mapped["User"] = relationship(
        back_populates="patient_appointments",
        foreign_keys=[patient_id],
    )

    professional: Mapped["ProfessionalProfile"] = relationship(
        back_populates="appointments",
        foreign_keys=[professional_id],
    )

    def __repr__(self) -> str:
        return (
            f"<Appointment(id={self.id}, patient_id={self.patient_id}, "
            f"professional_id={self.professional_id}, status={self.status})>"
        )
