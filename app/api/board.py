from typing import List
import random
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Form
from sqlalchemy.orm import Session
from app import crud, models, schemas
from ..database import SessionLocal, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from fastapi_utils.session import FastAPISessionMaker
models.Base.metadata.create_all(bind=engine)

# prefix used for all endpoints in this file
board = APIRouter(prefix="")
sessionmaker = FastAPISessionMaker("postgresql://postgres:postgres@10.5.0.5:5432/cd_api_db")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

init_messages = ["Někdo šuká na záchodech", "Osoby v kolejišti", "Zpoždění", "Nic nepřijelo",
                 "Přeházení čísel vagónů během jízdy", "Vlak netopí", "Vlak topí a nejde to vypnout",
                 "Výstup lidí uprostřed pole", "Přijely úplně jiný vagóny"]

@board.on_event("startup")
@repeat_every(seconds=86400)
def generate_new_board():
    with sessionmaker.context_session() as db:
        messages = crud.get_messages(db, 0)
        if len(messages) < 9:
            for m in init_messages:
                crud.create_message(db, m)
        board = crud.get_board(db)
        if board is not None:
            scores = crud.get_scores_by_board(db, board.id)
            for score in scores:
                todays_board = []
                messages = crud.get_messages(db, 0)
                for i in board.value.split():
                    todays_board.append(int(i))

                for idx, j in enumerate(score.value.split()):
                    if int(j) == 2:
                        crud.add_cntr_message(db, messages[todays_board[idx]].id)

        messages = crud.get_messages(db, 0)
        length = len(messages) - 1
        rands = []
        while len(rands) < 9:
            r1 = random.randint(0, length)
            if r1 not in rands:
                rands.append(r1)
        val = ' '.join(str(e) for e in rands)
        crud.create_board(db, val)
