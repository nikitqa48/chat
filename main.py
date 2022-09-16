from fastapi import FastAPI, WebSocket
from src import router
from src.chat.manager import ChatManager
from config.database import Base, engine


app = FastAPI()
app.include_router(router.router)
app.add_api_websocket_route('/ws/{token}/{room}/', ChatManager())


@app.on_event('startup')
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

