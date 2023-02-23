from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel


class MessageBase(BaseModel):
    text: str
    counter: int


class MessageCreate(MessageBase):
    pass


class Message(MessageCreate):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str
    role: str


class UserCreate(UserBase):
    pass


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


class BoardBase(BaseModel):
    date: datetime
    value: str


class BoardCreate(BoardBase):
    pass


class Board(BoardCreate):
    id: int

    class Config:
        orm_mode = True


class ScoreBase(BaseModel):
    date: datetime
    value: str
    user_id: int


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreCreate):
    id: int

    class Config:
        orm_mode = True
