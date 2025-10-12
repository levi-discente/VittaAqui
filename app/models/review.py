
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.professional import ProfessionalProfile
    from app.models.user import User


class Review(Base):

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"), unique=True, index=True
    )
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professional_profiles.id"), index=True
    )

    rating: Mapped[float] = mapped_column()
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_anonymous: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        back_populates="review",
        foreign_keys=[appointment_id],
    )

    patient: Mapped["User"] = relationship(
        back_populates="patient_reviews",
        foreign_keys=[patient_id],
    )

    professional: Mapped["ProfessionalProfile"] = relationship(
        back_populates="reviews",
        foreign_keys=[professional_id],
    )

    __table_args__ = (
        CheckConstraint("rating >= 1.0 AND rating <= 5.0", name="check_rating_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<Review(id={self.id}, appointment_id={self.appointment_id}, "
            f"rating={self.rating})>"
        )
