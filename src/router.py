from fastapi import APIRouter
from src.auth.endpoints import auth


router = APIRouter()
router.include_router(auth, tags=('auth',))
