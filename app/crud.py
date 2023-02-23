from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from . import models, schemas


def get_messages(db: Session, skip: int = 0):
    return db.query(models.Message).offset(skip).all()


def get_message(db: Session, id: int):
    return db.query(models.Message).filter(models.Message.id == id).first()


def delete_message(db: Session, id: int):
    db_mes = get_message(db, id)
    db.delete(db_mes)
    db.commit()
    return None


def create_message(db: Session, text: str):
    db_message = models.Message(text=text, counter=0)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def add_cntr_message(db: Session, message_id: int):
    old_message = get_message(db, message_id)
    new = {"id": old_message.id, "text": old_message.text, "counter": (old_message.counter + 1)}
    for key, value in new.items():
        setattr(old_message, key, value)
    db.commit()
    db.refresh(old_message)
    return old_message


def get_users(db: Session, skip: int = 0):
    return db.query(models.User).offset(skip).all()


def find_user(db: Session, name: str):
    return db.query(models.User).filter(models.User.username == name).first()


def find_user_byid(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def create_user(db: Session, name: str, passw: str, rol: str):
    db_user = models.User(username=name, password=passw, role=rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_board(db: Session, val: str):
    db_board = models.BingoBoard(value=val, date=datetime.now())
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def get_board(db: Session):
    db_board = db.query(models.BingoBoard).order_by(models.BingoBoard.id.desc()).first()
    return db_board


def get_scores_by_board(db: Session, board_id: int):
    scores = db.query(models.BingoScores).filter(models.BingoScores.board_id == board_id).all()
    return scores


def create_score(db: Session, val: str, user_id: int, board_id: int):
    db_score = models.BingoScores(value=val, date=datetime.now(), user_id=user_id, board_id=board_id)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def get_score(db: Session, score_id: int):
    return db.query(models.BingoScores).filter(models.BingoScores.id == score_id).first()


def update_score(db: Session, score_id: int, val: str):
    old_score = get_score(db, score_id)
    new = {"id": old_score.id, "value": val, "date": old_score.date, "user_id": old_score.user_id,
           "board:id": old_score.board_id}
    for key, value in new.items():
        setattr(old_score, key, value)
    db.commit()
    db.refresh(old_score)
    return old_score


def get_score_by_user(db: Session, username: str):
    user = find_user(db, username)
    score = db.query(models.BingoScores).order_by(models.BingoScores.id.desc()).filter(
        models.BingoScores.user_id == user.id).first()
    return score
