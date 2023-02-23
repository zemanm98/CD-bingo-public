import uvicorn
from fastapi import FastAPI
from app.api.main_web import main_web
from app.api.auth import auth
from app.api.message_web import messages_web
from app.api.board import board
app = FastAPI()

app.include_router(main_web)
app.include_router(auth)
app.include_router(messages_web)
app.include_router(board)

'''
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.22", port=8000)
'''

