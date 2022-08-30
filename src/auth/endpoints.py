from fastapi import APIRouter, Depends, HTTPException, status
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
