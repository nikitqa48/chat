from fastapi.security import OAuth2PasswordBearer
import requests


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_token(token):
    headers = {'Authorization': f"Token {token}"}
    request = requests.get(
        f'http://fatcode:8000/api/v1/auth/users/me/',
        headers=headers,
    )
    if request.status_code == 401:
        return False
    return True
