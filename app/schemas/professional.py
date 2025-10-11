
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ProfessionalCategory


class ProfileTagBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=50)


class ProfileTagCreate(ProfileTagBase):

    pass


class ProfileTagResponse(ProfileTagBase):

    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)


class UnavailableDateBase(BaseModel):

    date: str
    reason: str | None = Field(None, max_length=255)


class UnavailableDateCreate(UnavailableDateBase):

    pass


class UnavailableDateResponse(UnavailableDateBase):

    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)


class ProfessionalProfileBase(BaseModel):

    bio: str | None = None
    category: ProfessionalCategory
    profissional_identification: str = Field(..., min_length=1, max_length=50)
    services: str | None = None
    price: float = Field(default=0.0, ge=0)
    only_online: bool = False
    only_presential: bool = False
    available_days_of_week: str | None = None  # CSV: "monday,tuesday,wednesday"
    start_hour: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")  # "08:00"
    end_hour: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")  # "17:00"


class ProfessionalProfileCreate(ProfessionalProfileBase):

    tags: list[str] | None = None
    unavailable_dates: list[UnavailableDateCreate] | None = None


class ProfessionalProfileUpdate(BaseModel):

    bio: str | None = None
    category: ProfessionalCategory | None = None
    services: str | None = None
    price: float | None = Field(None, ge=0)
    only_online: bool | None = None
    only_presential: bool | None = None
    available_days_of_week: str | None = None
    start_hour: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_hour: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    tags: list[str] | None = None
    unavailable_dates: list[UnavailableDateCreate] | None = None


class ProfessionalProfileResponse(ProfessionalProfileBase):

    id: int
    user_id: int
    rating: float
    num_reviews: int

    user_name: str | None = None
    email: str | None = None
    phone: str | None = None
    cep: str | None = None
    uf: str | None = None
    city: str | None = None
    address: str | None = None

    tags: list[str] = []
    unavailable_dates: list[UnavailableDateResponse] = []

    model_config = ConfigDict(from_attributes=True)
