"""Enumerations for database models."""

from enum import Enum


class Role(str, Enum):
    """User role enumeration."""

    PATIENT = "patient"
    PROFESSIONAL = "professional"


class ProfessionalCategory(str, Enum):
    """Professional category enumeration."""

    NUTRITIONIST = "nutritionist"
    PERSONAL_TRAINER = "personal_trainer"
    PHYSICIAN = "physician"
    PSYCHOLOGIST = "psychologist"
    PHYSIOTHERAPIST = "physiotherapist"
    OCCUPATIONAL_THERAPY = "occupational_therapy"
    ELDERLY_CARE = "elderly_care"
    DOCTOR = "doctor"


class AppointmentStatus(str, Enum):
    """Appointment status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
