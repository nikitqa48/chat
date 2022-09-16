from fastapi import WebSocket
from collections import defaultdict
from src.chat import models
from sqlalchemy.future import select
from fastapi import Depends
from websockets_actions.fastapi.actions import WebSocketBroadcast
from sqlalchemy.orm import Session
from config.database import get_db
from src.middleware import get_user_by_token


async def get_or_create_user(data: str, db: Session = Depends(get_db)):
    user = await db.get(models.User, data['id'])
    if user is None:
        user = models.User(**data)
        db.add(user)
        await db.commit()
    return user


async def get_or_create_room(name: str, db: Session = Depends(get_db)):
    room = await db.execute(select(models.Room).where(models.Room.name == name))
    result = room.first()
    if result is None:
        result = models.Room(name=name)
        db.add(room)
        await db.commit()
    return result[0]


class ChatManager(WebSocketBroadcast):
    actions = ['send_message']

    def __init__(self):
        self.db_manager = DatabaseChatManager()

    async def send_message(self, websocket: WebSocket, data):
        await self.db_manager.send_message(data['text'])
        await self.manager.broadcast(data['text'])

    # async def connect(self, websocket: WebSocket, room: str, user: models.User):
    #     await websocket.accept()
    #     self.connections[room] = []
    #     self.connections[room].append((websocket, user))
    #
    # async def broadcast(self, data: str, room: str):
    #     for connection in self.connections[room]:
    #         await connection[0].send_json(data)

    # async def disconnect(self, websocket: WebSocket, room: str, user: models.User):
    #     self.connections[room].remove((websocket, user))

    async def __call__(
            self, websocket: WebSocket,
            room: str,
            token: str = Depends(get_user_by_token),
            db: Session = Depends(get_db),
    ):
        await self.db_manager.__connect_user__(token, room, db)
        await super().__call__(websocket)


class DatabaseChatManager:

    async def __connect_user__(
            self,
            user_json: str = Depends(get_or_create_user),
            room: str = Depends(get_or_create_room),
            db: Session = Depends(get_db)
    ):
        user = await get_or_create_user(user_json, db)
        self.user = user
        room = await get_or_create_room(room, db)
        self.room = room
        participiant_query = await db.execute(
            select(models.Participant).where(
                models.Participant.room_id == room.id
            ).where(
                models.Participant.user == user
            )
        )
        participiant = participiant_query.first()
        if participiant is None:
            await room.create_participiant(db, user)

    async def send_message(self, text):
        print(text)
        pass