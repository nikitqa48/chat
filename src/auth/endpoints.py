from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from src.middleware import oauth2_scheme, get_user_by_token
from src.auth.manager import ConnectionManager

auth = APIRouter()
manager = ConnectionManager()


@auth.websocket('/connect/{token}/{room}/')
async def websocket_endpoint(websocket: WebSocket, token: str, room: str):
    user = get_user_by_token(token)
    if user:
        await manager.connect(websocket, room, user)
        while True:
            try:
                data = await websocket.receive_text()
                response = {
                    "sender": user,
                    "message": data
                }
                await manager.broadcast(response, room)
            except WebSocketDisconnect:
                manager.disconnect(websocket, room, user)
                await manager.broadcast(f"Client #'{user}' left the chat", room)
            except RuntimeError:
                break
