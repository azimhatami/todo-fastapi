from fastapi import FastAPI

from app.routers.todo import todo


# App object
app = FastAPI()
app.include_router(todo)
