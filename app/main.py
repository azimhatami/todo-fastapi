from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers.todo import todo_router


# App object
app = FastAPI()
app.include_router(todo_router)

@app.get('/')
def root():
    return HTMLResponse('<center><h1>Welcome to fastAPI.</h1></center>')
