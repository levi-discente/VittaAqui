
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.enums import Role
from app.utils.validators import clean_cpf, validate_cpf


class UserBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    cpf: str = Field(..., min_length=11, max_length=14)
    phone: str | None = Field(None, max_length=20)
    cep: str | None = Field(None, max_length=10)
    uf: str | None = Field(None, max_length=2)
    city: str | None = Field(None, max_length=100)
    address: str | None = Field(None, max_length=255)
    profile_image_url: str | None = Field(None, max_length=500)

    @field_validator("cpf")
    @classmethod
    def validate_cpf_field(cls, v: str) -> str:
        cpf_clean = clean_cpf(v)
        if not validate_cpf(cpf_clean):
            raise ValueError("Invalid CPF")
        return cpf_clean


class UserCreate(UserBase):

    password: str = Field(..., min_length=8, max_length=100)
    role: Role
    profissional_identification: str | None = Field(None, max_length=50)
    category: str | None = Field(None, max_length=50)


class UserUpdate(BaseModel):

    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    cep: str | None = Field(None, max_length=10)
    uf: str | None = Field(None, max_length=2)
    city: str | None = Field(None, max_length=100)
    address: str | None = Field(None, max_length=255)


class UserResponse(UserBase):

    id: int
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):

    email: EmailStr
    password: str = Field(..., min_length=1)
