from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from src.middleware import get_user_by_token, oauth2_scheme
from src.chat.manager import ConnectionManager, get_or_create_user, get_or_create_room
from sqlalchemy.orm import Session
from config.database import get_db
from src.chat import models
from datetime import datetime
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
        # participials = manager.connections[room]
        # for participial in participials:
        #     """Нужно добавить всех участников комнаты в модель Participials"""
        #     print(participial[1])
        #     print('asds')
        while True:
            try:
                data = await websocket.receive_text()
                message = models.Message(author=user, room=room_obj, text=data, created=datetime.now())
                db.add(message)
                response = {
                    "sender": user_json['username'],
                    "message": data
                }
                db.commit()
                await manager.broadcast(response, room)
            except WebSocketDisconnect:
                manager.disconnect(websocket, room, user)
                await manager.broadcast(f"Client #'{user_json}' left the chat", room)
            except RuntimeError:
                break


@chat.get('/history/{room}/')
def get_history(room: str, token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    if not get_user_by_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
    messages = db.query(models.Message).all()
    data = []
    for message in messages:
        data.append(jsonable_encoder(message))
    return data
