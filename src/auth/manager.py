from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.connections.append((websocket, user))

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection[0].send_json(data)

    def disconnect(self, websocket: WebSocket, user: str):
        self.connections.remove((websocket, user))
