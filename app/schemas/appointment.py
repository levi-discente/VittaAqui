
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AppointmentStatus


class AppointmentBase(BaseModel):

    professional_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime


class AppointmentCreate(AppointmentBase):

    pass


class AppointmentUpdate(BaseModel):

    start_time: datetime | None = None
    end_time: datetime | None = None
    status: AppointmentStatus | None = None


class AppointmentResponse(BaseModel):

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
