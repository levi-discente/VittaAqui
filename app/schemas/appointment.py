
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import AppointmentStatus


class AppointmentBase(BaseModel):

    professional_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def remove_timezone(cls, v: datetime | str) -> datetime:
        if isinstance(v, str):
            # Parse string to datetime
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        else:
            dt = v
        
        # Remove timezone info
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt


class AppointmentCreate(AppointmentBase):

    pass


class AppointmentUpdate(BaseModel):

    start_time: datetime | None = None
    end_time: datetime | None = None
    status: AppointmentStatus | None = None

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def remove_timezone(cls, v: datetime | str | None) -> datetime | None:
        if v is None:
            return None
        
        if isinstance(v, str):
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
        else:
            dt = v

        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt


class AppointmentResponse(BaseModel):

    id: int
    patient_id: int
    patient_name: str | None = None
    patient_image_url: str | None = None
    professional_id: int
    professional_name: str | None = None
    professional_image_url: str | None = None
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
