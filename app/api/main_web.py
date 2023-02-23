from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter, Form
from sqlalchemy.orm import Session
from app import crud, models, schemas
from ..database import SessionLocal, engine
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

# Path to html templates used in this file
templates = Jinja2Templates(directory="templates/main")

# prefix used for all endpoints in this file
main_web = APIRouter(prefix="")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


selected_tiles = [1, 1, 1, 1, 1, 1, 1, 1, 1]
tiles_messages = ["Kuba", "je", "ten", "uplně", "největší", "gay", "na", "celim", "světě"]


@main_web.get("/", response_class=HTMLResponse)
async def show_bingo(request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user == None:
        return RedirectResponse(url=f"/login", status_code=303)

    if current_user == "admin":
        return templates.TemplateResponse("main.html", {"request": request, "selected_tiles": selected_tiles,
                                                        "messages": tiles_messages})
    else:
        board = crud.get_board(db)
        user = crud.find_user(db, current_user)
        if user == None:
            return RedirectResponse(url=f"/login", status_code=303)
        user_board = crud.get_score_by_user(db, user.username)
        if user_board is None or board.id != user_board.board_id:
            user_board = crud.create_score(db, "1 1 1 1 1 1 1 1 1", user.id, board.id)
        messages = crud.get_messages(db, 0)
        mess = []
        for i in board.value.split():
            mess.append(messages[int(i)].text)
        tiles = []
        for j in user_board.value.split():
            tiles.append(int(j))
        return templates.TemplateResponse("main.html", {"request": request, "selected_tiles": tiles,
                                                        "messages": mess})


@main_web.post("/bingo/{tile_id}", response_class=HTMLResponse)
async def clicked_tile(request: Request, tile_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user == None:
        return RedirectResponse(url=f"/login", status_code=303)

    if current_user == "admin":
        return templates.TemplateResponse("main.html", {"request": request, "selected_tiles": selected_tiles,
                                                        "messages": tiles_messages})
    else:
        board = crud.get_board(db)
        user = crud.find_user(db, current_user)
        if user == None:
            return RedirectResponse(url=f"/login", status_code=303)
        user_board = crud.get_score_by_user(db, user.username)
        if user_board is None or board.id != user_board.board_id:
            user_board = crud.create_score(db, "1 1 1 1 1 1 1 1 1", user.id, board.id)
        messages = crud.get_messages(db, 0)
        mess = []
        for i in board.value.split():
            mess.append(messages[int(i)].text)
        tiles = []
        for j in user_board.value.split():
            tiles.append(int(j))
        tiles[tile_id] = 3 - tiles[tile_id]
        val = ' '.join(str(e) for e in tiles)
        crud.update_score(db, user_board.id, val)
        return templates.TemplateResponse("main.html", {"request": request, "selected_tiles": tiles,
                                                        "messages": mess})
