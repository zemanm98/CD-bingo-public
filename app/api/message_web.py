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
templates = Jinja2Templates(directory="templates/message")

# prefix used for all endpoints in this file
messages_web = APIRouter(prefix="")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@messages_web.get("/messages", response_class=HTMLResponse)
async def read_devices(request: Request, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    current_messages = crud.get_messages(db, 0)
    if current_user != "admin":
        return templates.TemplateResponse("messages_normal.html", {"request": request, "messages": current_messages})
    else:
        return templates.TemplateResponse("messages.html", {"request": request, "messages": current_messages})


@messages_web.get("/messages-add", response_class=HTMLResponse)
async def read_devices(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user != "admin":
        return RedirectResponse(url=f"/", status_code=303)
    return templates.TemplateResponse("message_add.html", {"request": request})


@messages_web.post("/messages-add-con")
async def read_devices(db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),
                       text: str = Form(...)):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user != "admin":
        return RedirectResponse(url=f"/", status_code=303)
    crud.create_message(db, text)
    return RedirectResponse(url=f"/messages", status_code=303)

@messages_web.post("/messages-del/{mes_id}")
async def read_devices(mes_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user = Authorize.get_jwt_subject()
    if current_user != "admin":
        return RedirectResponse(url=f"/", status_code=303)
    crud.delete_message(db, mes_id)
    return RedirectResponse(url=f"/messages", status_code=303)
