from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    content: str
    temp_id: Optional[str] = None  # For client-side message reconciliation
    # File attachment fields
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class ChatMessageResponse(BaseModel):
    id: int
    appointment_id: int
    sender_user_id: int
    sender_name: str
    sender_image_url: Optional[str]
    content: str
    created_at: datetime
    temp_id: Optional[str] = None  # Echo back temp_id if provided
    # File attachment fields
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None

    class Config:
        from_attributes = True


class ChatMessageWebSocketMessage(BaseModel):
    """WebSocket message format for sending messages."""
    content: str
    temp_id: Optional[str] = None
    # File attachment fields
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
