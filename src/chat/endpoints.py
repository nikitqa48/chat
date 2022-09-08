from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from src.middleware import get_user_by_token, oauth2_scheme
from src.chat.manager import ConnectionManager, get_or_create_user, get_or_create_room
from sqlalchemy.orm import Session
from config.database import get_db
from src.chat import models
from fastapi.encoders import jsonable_encoder


chat = APIRouter()
manager = ConnectionManager()


@chat.websocket('/connect/{token}/{room}/')
async def websocket_endpoint(websocket: WebSocket, token: str, room: str, db: Session = Depends(get_db)):
    user_json = get_user_by_token(token)
    if user_json:
        user = get_or_create_user(db, user_json)
        room_obj = get_or_create_room(db, room)
        await manager.connect(websocket, room, user)
        # connections = manager.connections[room]
        participiants = db.query(models.Participant).filter_by(room=room_obj).all()
        if not participiants or not any(user == x.user for x in participiants):
            # Если нет участников в комнате, то создать участника в бд
            room_obj.create_participiant(db, user)
        while True:
            try:
                data = await websocket.receive_text()
                user.create_message(db, room_obj, data)
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


@chat.get('/history/{room}/')
def get_history(room: str, token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    get_user = get_user_by_token(token)
    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
    user = db.query(models.User).get(get_user['id'])
    room = db.query(models.Room).filter_by(name=room).first()
    participiant = db.query(models.Participant).filter_by(room=room, user=user).first()
    if participiant is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    messages = db.query(models.Message).filter_by(room=room).all()
    data = []
    for message in messages:
        data.append(jsonable_encoder(message))
    return data
