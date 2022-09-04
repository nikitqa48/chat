from fastapi import APIRouter
from src.chat.endpoints import chat


router = APIRouter()
router.include_router(chat, tags=('chat',))
