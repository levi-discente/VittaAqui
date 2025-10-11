"""Authentication schemas."""

from pydantic import BaseModel

from app.schemas.user import UserResponse


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    id: int
    email: str
    role: str


class LoginResponse(BaseModel):
    """Login response with token and user data."""

    token: str
    user: UserResponse
