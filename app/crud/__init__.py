"""CRUD operations (Repository pattern)."""

from app.crud.appointment import appointment_crud
from app.crud.professional import professional_crud
from app.crud.user import user_crud

__all__ = [
    "user_crud",
    "professional_crud",
    "appointment_crud",
]
