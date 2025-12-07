import json
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.websocket import manager
from app.models.user import User
from app.schemas.chat_message import ChatMessageWebSocketMessage
from app.services import chat as chat_service
from app.services.auth import get_current_user_from_token
from app.utils.exceptions import ForbiddenException, NotFoundException

router = APIRouter()


async def get_current_user_ws(token: str, db: AsyncSession) -> Optional[User]:
    """Get current user from WebSocket token parameter."""
    try:
        return await get_current_user_from_token(token, db)
    except Exception:
        return None


@router.websocket("/ws/chat/{appointment_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    appointment_id: int,
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """WebSocket endpoint for real-time chat."""
    
    # Authenticate user
    current_user = await get_current_user_ws(token, db)
    if not current_user:
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Validate chat access
    try:
        await chat_service.validate_chat_access(db, appointment_id, current_user)
    except (NotFoundException, ForbiddenException) as e:
        await websocket.close(code=1008, reason=str(e))
        return
    
    # Connect to room
    await manager.connect(websocket, appointment_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                ws_message = ChatMessageWebSocketMessage(**message_data)
            except (json.JSONDecodeError, ValueError) as e:
                await manager.send_personal_message(
                    json.dumps({"error": f"Invalid message format: {str(e)}"}),
                    websocket
                )
                continue
            
            # Validate content
            if not ws_message.content.strip():
                await manager.send_personal_message(
                    json.dumps({"error": "Message content cannot be empty"}),
                    websocket
                )
                continue
            
            # Create message in database
            try:
                message_response = await chat_service.create_chat_message(
                    db, 
                    appointment_id, 
                    current_user, 
                    ws_message.content.strip(),
                    ws_message.temp_id,
                    ws_message.file_url,
                    ws_message.file_name,
                    ws_message.file_type,
                    ws_message.file_size
                )
                
                # Broadcast to all connections in the room
                await manager.broadcast_to_room(
                    json.loads(message_response.model_dump_json()), 
                    appointment_id
                )
                
            except Exception as e:
                await manager.send_personal_message(
                    json.dumps({"error": f"Failed to send message: {str(e)}"}),
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, appointment_id)
