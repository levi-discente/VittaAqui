
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1.0 to 5.0")
    comment: str | None = Field(None, max_length=2000)
    is_anonymous: bool = Field(default=False)


class ReviewCreate(ReviewBase):
    appointment_id: int = Field(..., gt=0)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: float) -> float:
        if v < 1.0 or v > 5.0:
            raise ValueError("Rating must be between 1.0 and 5.0")
        return round(v, 1)


class ReviewUpdate(BaseModel):
    rating: float | None = Field(None, ge=1.0, le=5.0)
    comment: str | None = Field(None, max_length=2000)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: float | None) -> float | None:
        if v is not None:
            if v < 1.0 or v > 5.0:
                raise ValueError("Rating must be between 1.0 and 5.0")
            return round(v, 1)
        return v


class PatientInfo(BaseModel):
    id: int
    name: str
    profile_image_url: str | None = None

    model_config = {"from_attributes": True}


class ReviewResponse(ReviewBase):
    id: int
    appointment_id: int
    patient_id: int
    professional_id: int
    patient: PatientInfo | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReviewList(BaseModel):
    total: int
    items: list[ReviewResponse]


class ReviewStats(BaseModel):
    average_rating: float
    total_reviews: int
    distribution: dict[str, int] = Field(
        default_factory=dict,
        description="Distribution of ratings (1-5 stars)",
    )

    model_config = {"from_attributes": True}
