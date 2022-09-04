from fastapi.security import OAuth2PasswordBearer
import requests
import json


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_token(token):
    headers = {'Authorization': f"Token {token}"}
    request = requests.get(
        'http://fatcode:8000/api/v1/auth/users/me/',
        headers=headers,
    )
    if request.status_code == 401:
        return False
    user = json.loads(request.content)
    return user

