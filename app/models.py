from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)

    scores = relationship("BingoScores", back_populates="users")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=False)
    counter = Column(Integer, index=True, nullable=False)


class BingoBoard(Base):
    __tablename__ = "bingo-board"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    scores = relationship("BingoScores", back_populates="boards")

class BingoScores(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    board_id = Column(Integer, ForeignKey("bingo-board.id"))

    users = relationship("User", back_populates="scores")
    boards = relationship("BingoBoard", back_populates="scores")
