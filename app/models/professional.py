"""Professional profile models."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ProfessionalCategory

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.user import User


class ProfessionalProfile(Base):
    """Professional profile model."""

    __tablename__ = "professional_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)

    # Professional information
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[ProfessionalCategory] = mapped_column(String(50))
    profissional_identification: Mapped[str] = mapped_column(String(50), unique=True)
    services: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(default=0.0)

    # Service type
    only_online: Mapped[bool] = mapped_column(default=False)
    only_presential: Mapped[bool] = mapped_column(default=False)

    # Rating
    rating: Mapped[float] = mapped_column(default=0.0)
    num_reviews: Mapped[int] = mapped_column(default=0)

    # Availability
    available_days_of_week: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # CSV: "monday,tuesday,wednesday"
    start_hour: Mapped[str | None] = mapped_column(String(5), nullable=True)  # "08:00"
    end_hour: Mapped[str | None] = mapped_column(String(5), nullable=True)  # "17:00"

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="professional_profile")

    tags: Mapped[list["ProfileTag"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    unavailable_dates: Mapped[list["UnavailableDate"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="professional",
        foreign_keys="Appointment.professional_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<ProfessionalProfile(id={self.id}, category={self.category})>"


class ProfileTag(Base):
    """Tags for professional profiles."""

    __tablename__ = "profile_tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("professional_profiles.id"), index=True)
    name: Mapped[str] = mapped_column(String(50))

    # Relationship
    profile: Mapped["ProfessionalProfile"] = relationship(back_populates="tags")

    def __repr__(self) -> str:
        return f"<ProfileTag(id={self.id}, name={self.name})>"


class UnavailableDate(Base):
    """Unavailable dates for professionals."""

    __tablename__ = "unavailable_dates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("professional_profiles.id"), index=True)
    date: Mapped[datetime] = mapped_column()
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationship
    profile: Mapped["ProfessionalProfile"] = relationship(back_populates="unavailable_dates")

    def __repr__(self) -> str:
        return f"<UnavailableDate(id={self.id}, date={self.date})>"
