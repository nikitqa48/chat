from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from src.middleware import get_user_by_token, oauth2_scheme
from src.chat.manager import ConnectionManager, get_or_create_user, get_or_create_room
from sqlalchemy.orm import Session
from config.database import get_db
from src.chat import models
from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select


chat = APIRouter()
manager = ConnectionManager()


@chat.websocket('/connect/{token}/{room}/')
async def websocket_endpoint(websocket: WebSocket, token: str, room: str, db: Session = Depends(get_db)):
    user_json = get_user_by_token(token)
    user = await get_or_create_user(db, user_json)
    await manager.connect(websocket, room, user)
    while True:
        try:
            data = await websocket.receive_text()
            # await user.create_message(db, room_obj, data)
            response = {
                "sender": user_json['username'],
                "message": data
                }
            await manager.broadcast(response, room)
        except WebSocketDisconnect:
            await manager.disconnect(websocket, room, user)
            await manager.broadcast(f"Client #'{user_json}' left the chat", room)
        except RuntimeError:
            break

    # user_json = get_user_by_token(token)
    # if user_json:
    #     user = await get_or_create_user(db, user_json)
    #     room_obj = await get_or_create_room(db, room)
    #     members = db.query(models.Participant).filter_by(room=room_obj).all()
    #     if not members or not any(user == x.user for x in members):
    #         # Если нет участников в комнате, то создать участника в бд
    #         room_obj.create_participiant(db, user)
    #     await manager.connect(websocket, room, user)
    #     while True:
    #         try:
    #             data = await websocket.receive_text()
    #             await user.create_message(db, room_obj, data)
    #             response = {
    #                 "sender": user_json['username'],
    #                 "message": data
    #             }
    #             await manager.broadcast(response, room)
    #         except WebSocketDisconnect:
    #             await manager.disconnect(websocket, room, user)
    #             await manager.broadcast(f"Client #'{user_json}' left the chat", room)
    #         except RuntimeError:
    #             break


@chat.get('/history/{room}/')
async def get_history(room: str, token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    get_user = get_user_by_token(token)
    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
    user = await db.get(models.User, get_user['id'])
    room_obj = await db.execute(select(models.Room).where(models.Room.name == room))
    participiant = await db.execute(select(models.Participant).where(models.Room == room_obj.first(), user == user))
    if participiant.first() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not access"
        )
    messages = await db.execute(select(models.Message).where(models.Room == room))
    data = []
    for message in messages.all():
        data.append(jsonable_encoder(message))
    return data
