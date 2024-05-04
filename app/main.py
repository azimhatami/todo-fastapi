from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId


# App object
app = FastAPI()

client = MongoClient('mongodb://todo_fastapi-mongo-1:27017')
db = client['todo_db']
collection = db['todo_collection']


# ToDo model
class ToDo(BaseModel):
    title: str
    description: str


@app.post('/todos/')
async def create_todo(todo: ToDo):
    '''
    Create a new ToDo item.
    '''
    todo_data = {
        'title': todo.title,
        'description': todo.description,
    }
    result = collection.insert_one(todo_data)
    return {
        '_id': str(result.inserted_id),
        'title': todo.title,
        'description': todo.description,
    }

@app.get('/todos/')
async def get_todos():
    '''
    Get all ToDo items.
    '''
    todos = []
    for todo in collection.find():
        todos.append({
            '_id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description']
        })
    return todos


@app.get('/todos/{todo_id}/')
async def get_todo(todo_id: str):
    '''
    Get a specific ToDo item by ID.
    '''
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail='Invalid todo_id')
    todo = collection.find_one({'_id': ObjectId(todo_id)})
    if todo:
        return {
            '_id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description']
        }
    else:
        raise HTTPException(status_code=404, detail='ToDo Not found')

@app.put('/todos/update/{todo_id}/')
async def update_todo(todo_id: str, todo: ToDo):
    '''
    Update a ToDo item by ID.
    '''
    existing_todo = collection.find_one({'_id': ObjectId(todo_id)})
    if existing_todo:
        result = collection.update_one(
            {'_id': ObjectId(todo_id)},
            {'$set': todo.dict()},
        )
        if result.modified_count == 1:
            raise HTTPException(status_code=200, detail='ToDo updated successfully')
    raise HTTPException(status_code=404, detail='ToDo Not found')

@app.delete('/todos/delete/{todo_id}')
async def delete_todo(todo_id: str):
    '''
    Delete a ToDo item by ID.
    '''
    result = collection.delete_one({'_id': ObjectId(todo_id)})
    if result.deleted_count == 1:
        raise HTTPException(status_code=200, detail='ToDo deleted successfully')
    else:
        raise HTTPException(status_code=404, detail='ToDo Not found')
