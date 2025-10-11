
from enum import Enum


class Role(str, Enum):

    PATIENT = "patient"
    PROFESSIONAL = "professional"


class ProfessionalCategory(str, Enum):

    NUTRITIONIST = "nutritionist"
    PERSONAL_TRAINER = "personal_trainer"
    PHYSICIAN = "physician"
    PSYCHOLOGIST = "psychologist"
    PHYSIOTHERAPIST = "physiotherapist"
    OCCUPATIONAL_THERAPY = "occupational_therapy"
    ELDERLY_CARE = "elderly_care"
    DOCTOR = "doctor"


class AppointmentStatus(str, Enum):

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
