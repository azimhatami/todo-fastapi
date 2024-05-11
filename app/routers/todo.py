from fastapi import APIRouter

from app.repository.todo import ToDoRepository
from app.data_adapter.db import collection
from app.schemas.todo import ToDo


todo_router = APIRouter()

todo_repository = ToDoRepository(collection)

@todo_router.post('/todos/')
async def create_todo(
    todo: ToDo,
):
    return todo_repository.create_todo(todo)

@todo_router.get('/todos/',)
async def get_todos():
    return todo_repository.get_all_todos()

@todo_router.get('/todos/{todo_id}', response_model=ToDo)
async def get_todo(todo_id: str):
    return todo_repository.get_todo_by_id(todo_id)

@todo_router.put('/todos/update/{todo_id}', response_model=list[ToDo])
async def update_todo(todo_id: str, todo: ToDo):
    return todo_repository.update_todo(todo_id, todo)

@todo_router.delete('/todos/delete/{todo_id}')
async def delete_todo(todo_id: str):
    return todo_repository.delete_todo(todo_id)
