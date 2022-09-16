from fastapi.security import OAuth2PasswordBearer
from fastapi import WebSocket
from starlette import status
import requests
import json


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_by_token(
        websocket: WebSocket,
        token: str,
        ):
    headers = {'Authorization': f"Token {token}"}
    request = requests.get(
        'http://fatcode:8000/api/v1/auth/users/me/',
        headers=headers,
    )
    if request.status_code == 401:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    user = json.loads(request.content)
    return user

