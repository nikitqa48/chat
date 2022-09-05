from fastapi import WebSocket
from collections import defaultdict
from src.chat import models


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

    def disconnect(self, websocket: WebSocket, room: str, user: models.User):
        self.connections[room].remove((websocket, user))


def get_or_create_user(db, json):
    try:
        user = db.query(models.User).get(json['id'])
    except:
        user = models.User(**json)
        db.add(user)
        db.commit()
    return user


def get_or_create_room(db, json):
    try:
        room = db.query(models.Room).get(name=json)
    except:
        room = models.Room(name=json)
        db.add(room)
        db.commit()
    return room


def get_or_create_particials(db, data):
    pass
