from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    middle_name: str
    avatar: str

    class Config:
        orm_mode = True


class Room(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Message(BaseModel):
    id: int
    author: User
    text: str
    created: datetime
    updated: datetime
    read: bool

    class Config:
        orm_mode = True


class Participant(BaseModel):
    id: int
    user: User
    room: Room

    class Config:
        orm_mode = True
