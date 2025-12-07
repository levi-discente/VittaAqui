from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.appointment import appointment_crud
from app.crud.chat_message import chat_message_crud
from app.models.appointment import Appointment
from app.models.chat_message import ChatMessage
from app.models.enums import AppointmentStatus
from app.models.user import User
from app.schemas.chat_message import ChatMessageResponse
from app.services.s3 import s3_service
from app.utils.exceptions import ForbiddenException, NotFoundException


async def validate_chat_access(
    db: AsyncSession, appointment_id: int, user: User
) -> Appointment:
    """
    Validate that the user can access chat for this appointment.
    
    Rules:
    1. Appointment must exist
    2. Appointment status must be CONFIRMED
    3. User must be either the patient or the professional
    
    Returns the appointment if valid, raises exception otherwise.
    """
    appointment = await appointment_crud.get_with_relations(db, appointment_id=appointment_id)
    if not appointment:
        raise NotFoundException("Appointment not found")
    
    if appointment.status != AppointmentStatus.CONFIRMED:
        raise ForbiddenException("Chat is only available for confirmed appointments")
    
    # Check if user is participant
    is_patient = appointment.patient_id == user.id
    is_professional = (
        appointment.professional 
        and appointment.professional.user_id == user.id
    )
    
    if not (is_patient or is_professional):
        raise ForbiddenException("You are not authorized to access this chat")
    
    return appointment


async def validate_chat_history_access(
    db: AsyncSession, appointment_id: int, user: User
) -> Appointment:
    """
    Validate that the user can view chat history for this appointment.
    
    Rules:
    1. Appointment must exist
    2. User must be either the patient or the professional
    3. No status restriction (can view history for any appointment)
    
    Returns the appointment if valid, raises exception otherwise.
    """
    appointment = await appointment_crud.get_with_relations(db, appointment_id=appointment_id)
    if not appointment:
        raise NotFoundException("Appointment not found")
    
    # Check if user is participant
    is_patient = appointment.patient_id == user.id
    is_professional = (
        appointment.professional 
        and appointment.professional.user_id == user.id
    )
    
    if not (is_patient or is_professional):
        raise ForbiddenException("You are not authorized to access this chat")
    
    return appointment


async def get_chat_messages(
    db: AsyncSession, appointment_id: int, user: User, skip: int = 0, limit: int = 100
) -> list[ChatMessageResponse]:
    """Get chat messages for an appointment."""
    # Validate access for history viewing (allows any appointment status)
    await validate_chat_history_access(db, appointment_id, user)
    
    # Get messages
    messages = await chat_message_crud.get_by_appointment(
        db, appointment_id, skip=skip, limit=limit
    )
    
    # Convert to response format
    return [
        ChatMessageResponse(
            id=msg.id,
            appointment_id=msg.appointment_id,
            sender_user_id=msg.sender_user_id,
            sender_name=msg.sender.name,
            sender_image_url=msg.sender.profile_image_url,
            content=msg.content,
            created_at=msg.created_at,
            file_url=msg.file_url,
            file_name=msg.file_name,
            file_type=msg.file_type,
            file_size=msg.file_size,
        )
        for msg in messages
    ]


async def create_chat_message(
    db: AsyncSession, 
    appointment_id: int, 
    user: User, 
    content: str,
    temp_id: str = None,
    file_url: str = None,
    file_name: str = None,
    file_type: str = None,
    file_size: int = None
) -> ChatMessageResponse:
    """Create a new chat message."""
    # Validate access first
    await validate_chat_access(db, appointment_id, user)
    
    # Create message
    message = await chat_message_crud.create(
        db, 
        appointment_id=appointment_id, 
        sender_user_id=user.id, 
        content=content,
        file_url=file_url,
        file_name=file_name,
        file_type=file_type,
        file_size=file_size
    )
    
    # Load sender info for response
    await db.refresh(message, ["sender"])
    
    return ChatMessageResponse(
        id=message.id,
        appointment_id=message.appointment_id,
        sender_user_id=message.sender_user_id,
        sender_name=message.sender.name,
        sender_image_url=message.sender.profile_image_url,
        content=message.content,
        created_at=message.created_at,
        temp_id=temp_id,
        file_url=message.file_url,
        file_name=message.file_name,
        file_type=message.file_type,
        file_size=message.file_size,
    )
