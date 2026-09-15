"""
Real-time WebSocket Connection Manager.
Supports topic-based pub/sub for order tracking, seller alerts, and admin notifications.
"""

from typing import Dict, List, Set, Any
from fastapi import WebSocket
from app.core.logging import logger
import json


class ConnectionManager:
    def __init__(self):
        # Maps topic -> set of WebSockets
        self.active_topics: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, topic: str):
        await websocket.accept()
        if topic not in self.active_topics:
            self.active_topics[topic] = set()
        self.active_topics[topic].add(websocket)
        logger.info(f"WebSocket client connected to topic '{topic}'. Active subscribers: {len(self.active_topics[topic])}")

    def disconnect(self, websocket: WebSocket, topic: str):
        if topic in self.active_topics and websocket in self.active_topics[topic]:
            self.active_topics[topic].remove(websocket)
            if not self.active_topics[topic]:
                del self.active_topics[topic]
        logger.info(f"WebSocket client disconnected from topic '{topic}'")

    async def broadcast_to_topic(self, topic: str, message: Any):
        """Send a JSON message to all subscribers of a specific topic."""
        if topic in self.active_topics:
            payload = json.dumps(message) if not isinstance(message, str) else message
            dead_sockets = []
            for connection in self.active_topics[topic]:
                try:
                    await connection.send_text(payload)
                except Exception as e:
                    logger.warning(f"Error sending message on topic '{topic}': {e}")
                    dead_sockets.append(connection)
            for dead in dead_sockets:
                self.disconnect(dead, topic)

    async def broadcast_system_alert(self, title: str, message: str, level: str = "INFO"):
        """Broadcast an alert to the admin channel."""
        await self.broadcast_to_topic("admin_channel", {
            "type": "SYSTEM_ALERT",
            "level": level,
            "title": title,
            "message": message
        })


ws_manager = ConnectionManager()

# Topic-based pub/sub broadcast for connected client sockets

# Ping/pong timeout disconnection to prevent memory leaks
