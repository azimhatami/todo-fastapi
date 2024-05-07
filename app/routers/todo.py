from fastapi import APIRouter, Depends

from app.repository.todo import ToDoRepository
from app.data_adapter.db import collection
from app.schemas.todo import ToDo


todo = APIRouter()

# Dependency injection for cleaner API routes
todo_repository = ToDoRepository(collection)

@todo.post('/todos/')
async def create_todo(
    todo: ToDo,
    todo_repo: ToDoRepository = Depends(todo_repository)
):
    '''
    Create a new ToDo item.
    '''
    print('Routers Ok')
    return todo_repo('create_todo', todo)

@todo.get('/todos/')
async def get_todos(todo_repo: ToDoRepository = Depends(todo_repository)):
    '''
    Get all ToDo items.
    '''
    print('Routers Ok')
    return todo_repo('get_all_todos')

@todo.get('/todos/{todo_id}')
async def get_todo(
    todo_id: str,
    todo_repo: ToDoRepository = Depends(todo_repository)
):
    '''
    Get a specific ToDo item by ID.
    '''
    print('Routers Ok')
    return todo_repo('get_todo_by_id', todo_id)

@todo.put('/todos/update/{todo_id}')
async def update_todo(
    todo_id: str,
    todo: ToDo,
    todo_repo: ToDoRepository = Depends(todo_repository)
):
    '''
    update a ToDo item by ID.
    '''
    print('Routers Ok')
    return todo_repo('update_todo', todo_id, todo)

@todo.delete('/todos/delete/{todo_id}')
async def delete_todo(
    todo_id: str,
    todo_repo: ToDoRepository = Depends(todo_repository)
):
    '''
    Delete a ToDo item by ID.
    '''
    print('Routers Ok')
    return todo_repo('delete_todo', todo_id)

