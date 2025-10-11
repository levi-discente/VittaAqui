"""Pydantic schemas for request/response validation."""

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)
from app.schemas.auth import LoginResponse, Token, TokenData
from app.schemas.professional import (
    ProfessionalProfileCreate,
    ProfessionalProfileResponse,
    ProfessionalProfileUpdate,
    ProfileTagCreate,
    ProfileTagResponse,
    UnavailableDateCreate,
    UnavailableDateResponse,
)
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    # Auth
    "Token",
    "TokenData",
    "LoginResponse",
    # Professional
    "ProfessionalProfileCreate",
    "ProfessionalProfileUpdate",
    "ProfessionalProfileResponse",
    "ProfileTagCreate",
    "ProfileTagResponse",
    "UnavailableDateCreate",
    "UnavailableDateResponse",
    # Appointment
    "AppointmentCreate",
    "AppointmentUpdate",
    "AppointmentResponse",
]
