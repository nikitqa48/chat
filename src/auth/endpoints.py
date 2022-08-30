from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from src.middleware import oauth2_scheme, validate_token

auth = APIRouter()


@auth.get('/')
def hello_world(token: str = Depends(oauth2_scheme)):
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
    return 'ok'


@auth.websocket('/ws/')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
