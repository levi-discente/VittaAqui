from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services import user as user_service
from app.utils.exceptions import ForbiddenException

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentUser,
):
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_in: UserUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await user_service.update_user(db, current_user.id, user_in)
    return UserResponse.model_validate(user)


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await user_service.delete_user(db, current_user.id)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.id != user_id:
        raise ForbiddenException("Not authorized to view this user")

    user = await user_service.get_user(db, user_id)
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
async def list_users(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    users = await user_service.get_all_users(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.id != user_id:
        raise ForbiddenException("Not authorized to update this user")

    user = await user_service.update_user(db, user_id, user_in)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if current_user.id != user_id:
        raise ForbiddenException("Not authorized to delete this user")

    await user_service.delete_user(db, user_id)


@router.post("/me/profile-image", response_model=UserResponse)
async def upload_my_profile_image(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
):
    """Upload profile image for the current user."""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Uploading image for user {current_user.id}")
        logger.info(f"File: {file.filename}, Content-Type: {file.content_type}")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            logger.error(f"Invalid file type: {file.content_type}")
            raise ForbiddenException("Only image files are allowed")

        # Read file content
        file_content = await file.read()
        logger.info(f"File size: {len(file_content)} bytes")

        # Upload image
        user = await user_service.upload_profile_image(
            db, current_user.id, file_content, file.filename or "profile.jpg"
        )
        
        logger.info(f"Image uploaded successfully: {user.profile_image_url}")
        return UserResponse.model_validate(user)
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}", exc_info=True)
        raise
