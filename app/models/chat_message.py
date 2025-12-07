from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.user import User


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"), index=True)
    sender_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, index=True)
    
    # File attachment fields
    file_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        back_populates="chat_messages",
        foreign_keys=[appointment_id],
    )
    
    sender: Mapped["User"] = relationship(
        foreign_keys=[sender_user_id],
    )

    def __repr__(self) -> str:
        return (
            f"<ChatMessage(id={self.id}, appointment_id={self.appointment_id}, "
            f"sender_user_id={self.sender_user_id})>"
        )
