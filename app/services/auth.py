
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.auth import LoginResponse
from app.schemas.user import UserResponse
from app.utils.exceptions import BadRequestException, UnauthorizedException


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await user_crud.get_by_email(db, email=email)

    if not user:
        raise UnauthorizedException("Invalid credentials")

    if not verify_password(password, user.password):
        raise UnauthorizedException("Invalid credentials")

    return user


async def login(db: AsyncSession, email: str, password: str) -> LoginResponse:
    user = await authenticate_user(db, email, password)

    role_value = user.role.value if hasattr(user.role, 'value') else user.role
    
    token_data = {
        "id": user.id,
        "email": user.email,
        "role": role_value,
        "name": user.name,
    }
    access_token = create_access_token(token_data)

    user_response = UserResponse.model_validate(user)
    return LoginResponse(token=access_token, user=user_response)


def hash_password(password: str) -> str:
    return get_password_hash(password)
