from fastapi import FastAPI, WebSocket
from config.database import SessionLocal, engine
from src.chat import models
from src import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router.router)
