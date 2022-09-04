from fastapi import WebSocket
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.connections: dict = defaultdict(dict)

    async def connect(self, websocket: WebSocket, room: str, user: dict):
        await websocket.accept()
        self.connections[room] = []
        self.connections[room].append((websocket, user))
        print(self.connections[room])

    async def broadcast(self, data: str, room: str):
        for connection in self.connections[room]:
            await connection[0].send_json(data)

    def disconnect(self, websocket: WebSocket, room: str, user: dict):
        self.connections[room].remove((websocket, user))
