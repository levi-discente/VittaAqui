from typing import Annotated

from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.schemas.chat_message import ChatMessageResponse
from app.services import chat as chat_service
from app.services.s3 import s3_service

router = APIRouter()


@router.get("/{appointment_id}/messages", response_model=list[ChatMessageResponse])
async def get_chat_messages(
    appointment_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """Get chat messages for an appointment."""
    return await chat_service.get_chat_messages(
        db, appointment_id, current_user, skip=skip, limit=limit
    )


@router.post("/{appointment_id}/upload-file", response_model=dict)
async def upload_chat_file(
    appointment_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
):
    """Upload a file for chat."""
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    
    # Validate access to the appointment
    await chat_service.validate_chat_access(db, appointment_id, current_user)
    
    try:
        # Upload to S3
        upload_result = s3_service.upload_chat_file(
            file_content=file_content,
            file_name=file.filename or "unknown",
            appointment_id=appointment_id
        )
        
        return {
            "file_url": upload_result["url"],
            "file_name": upload_result["file_name"],
            "file_type": upload_result["file_type"],
            "file_size": len(file_content),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
