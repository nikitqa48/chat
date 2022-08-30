from fastapi import FastAPI
from sqlalchemy import create_engine
from config.settings import settings
from src import router

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
app = FastAPI()
app.include_router(router.router)
