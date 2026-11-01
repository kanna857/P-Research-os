"""
WebSocket connection manager for real-time task progress and events.
"""

from typing import Dict, List, Any
import json
import asyncio
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        # Map of project_id or channel -> list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, channel: str = "global"):
        await websocket.accept()
        async with self.lock:
            if channel not in self.active_connections:
                self.active_connections[channel] = []
            self.active_connections[channel].append(websocket)

    async def disconnect(self, websocket: WebSocket, channel: str = "global"):
        async with self.lock:
            if channel in self.active_connections:
                if websocket in self.active_connections[channel]:
                    self.active_connections[channel].remove(websocket)
                if not self.active_connections[channel]:
                    del self.active_connections[channel]

    async def broadcast(self, message: Dict[str, Any], channel: str = "global"):
        payload = json.dumps(message)
        async with self.lock:
            connections = list(self.active_connections.get(channel, []))
            # Also broadcast to global if channel is specific
            if channel != "global" and "global" in self.active_connections:
                connections.extend(self.active_connections["global"])

        dead_connections = []
        for connection in connections:
            try:
                await connection.send_text(payload)
            except Exception:
                dead_connections.append(connection)

        if dead_connections:
            async with self.lock:
                for channel_key in list(self.active_connections.keys()):
                    self.active_connections[channel_key] = [
                        ws for ws in self.active_connections[channel_key] if ws not in dead_connections
                    ]
                    if not self.active_connections[channel_key]:
                        del self.active_connections[channel_key]


ws_manager = WebSocketManager()
