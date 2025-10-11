"""Appointment schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AppointmentStatus


class AppointmentBase(BaseModel):
    """Base schema for appointments."""

    professional_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime


class AppointmentCreate(AppointmentBase):
    """Schema for creating an appointment."""

    pass


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment."""

    start_time: datetime | None = None
    end_time: datetime | None = None
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):
    """Schema for appointment response."""

    id: int
    patient_id: int
    patient_name: str | None = None
    professional_id: int
    professional_name: str | None = None
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
