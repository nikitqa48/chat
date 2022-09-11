from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import Session
from config.database import get_db


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(300), index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    middle_name = Column(String(255))
    avatar = Column(String)

    async def create_message(self, db, room, text):
        message = Message(author=self, room=room, text=text, created=datetime.now())
        db.add(message)
        return db.commit()


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def create_participiant(self, db, user):
        participiant = Participant(room=self, user=user)
        db.add(participiant)
        return db.commit()


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    author = relationship('User', foreign_keys=[author_id])
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, index=True)
    room = relationship('Room', foreign_keys=[room_id])
    text = Column(String)
    created = Column(DateTime(timezone=True), index=True)
    updated = Column(DateTime(timezone=True))
    read = Column(Boolean)


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False, index=True)
    room = relationship('Room', foreign_keys=[room_id])
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = relationship('User', foreign_keys=[user_id])

