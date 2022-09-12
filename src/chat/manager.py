from fastapi import WebSocket
from collections import defaultdict
from src.chat import models
from sqlalchemy.future import select
from sqlalchemy import text


class ConnectionManager:
    def __init__(self):
        self.connections: dict = defaultdict(dict)

    async def connect(self, websocket: WebSocket, room: str, user: models.User):
        await websocket.accept()
        self.connections[room] = []
        self.connections[room].append((websocket, user))

    async def broadcast(self, data: str, room: str):
        for connection in self.connections[room]:
            await connection[0].send_json(data)

    async def disconnect(self, websocket: WebSocket, room: str, user: models.User):
        self.connections[room].remove((websocket, user))


async def get_or_create_user(db, data):
    user = await db.get(models.User, data['id'])
    if user is None:
        user = models.User(**data)
        db.add(user)
        await db.commit()
    return user


async def get_or_create_room(db, name: str):
    room = await db.execute(select(models.Room).where(models.Room.name == name))
    result = room.first()
    if result is None:
        result = models.Room(name=name)
        db.add(room)
        await db.commit()
    return result


