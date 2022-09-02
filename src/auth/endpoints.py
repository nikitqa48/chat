from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from src.middleware import oauth2_scheme, validate_token
from src.auth.manager import ConnectionManager

auth = APIRouter()
manager = ConnectionManager()


@auth.get('/')
def hello_world(token: str = Depends(oauth2_scheme)):
    return 'ok'


@auth.websocket('/connect/{token}/')
async def websocket_endpoint(websocket: WebSocket, token: str):
    if validate_token(token):
        await manager.connect(websocket, token)
        while True:
            try:
                data = await websocket.receive_text()
                response = {
                    "sender": token,
                    "message": data
                }
                await manager.broadcast(response)
            except WebSocketDisconnect:
                manager.disconnect(websocket, token)
                await manager.broadcast(f"Client #{token} left the chat")
            except RuntimeError:
                break
