import json
from typing import Dict, Set

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections for chat rooms."""
    
    def __init__(self):
        # appointment_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, appointment_id: int):
        """Accept a WebSocket connection and add to room."""
        await websocket.accept()
        if appointment_id not in self.active_connections:
            self.active_connections[appointment_id] = set()
        self.active_connections[appointment_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, appointment_id: int):
        """Remove a WebSocket connection from room."""
        if appointment_id in self.active_connections:
            self.active_connections[appointment_id].discard(websocket)
            # Clean up empty rooms
            if not self.active_connections[appointment_id]:
                del self.active_connections[appointment_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket."""
        try:
            await websocket.send_text(message)
        except Exception:
            # Connection might be closed
            pass
    
    async def broadcast_to_room(self, message: dict, appointment_id: int):
        """Broadcast a message to all connections in a room."""
        if appointment_id not in self.active_connections:
            return
        
        message_text = json.dumps(message)
        disconnected = set()
        
        for connection in self.active_connections[appointment_id]:
            try:
                await connection.send_text(message_text)
            except Exception:
                # Mark for removal if connection is dead
                disconnected.add(connection)
        
        # Clean up dead connections
        for connection in disconnected:
            self.active_connections[appointment_id].discard(connection)


# Global connection manager instance
manager = ConnectionManager()
