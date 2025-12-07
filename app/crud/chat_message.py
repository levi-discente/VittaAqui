from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat_message import ChatMessage


class ChatMessageCRUD:
    async def create(
        self,
        db: AsyncSession,
        appointment_id: int,
        sender_user_id: int,
        content: str,
        file_url: str = None,
        file_name: str = None,
        file_type: str = None,
        file_size: int = None,
    ) -> ChatMessage:
        """Create a new chat message."""
        message = ChatMessage(
            appointment_id=appointment_id,
            sender_user_id=sender_user_id,
            content=content,
            file_url=file_url,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    async def get_by_appointment(
        self,
        db: AsyncSession,
        appointment_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ChatMessage]:
        """Get messages for an appointment, ordered by created_at ASC."""
        stmt = (
            select(ChatMessage)
            .options(selectinload(ChatMessage.sender))
            .where(ChatMessage.appointment_id == appointment_id)
            .order_by(ChatMessage.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(
        self, db: AsyncSession, message_id: int
    ) -> Optional[ChatMessage]:
        """Get a message by ID."""
        stmt = select(ChatMessage).where(ChatMessage.id == message_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


chat_message_crud = ChatMessageCRUD()
