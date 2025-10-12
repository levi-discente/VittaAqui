
from pydantic import BaseModel

from app.schemas.user import UserResponse


class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):

    id: int
    email: str
    role: str


class LoginResponse(BaseModel):

    token: str
    user: UserResponse
