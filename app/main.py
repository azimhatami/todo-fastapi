from fastapi import FastAPI
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


@app.post('/todos')
async def create_todo(todo: ToDo):
    result = collection.insert_one(todo.dict())
    return {
        '_id': str(result.inserted_id),
        'title': todo.title,
        'description': todo.description,
    }

@app.get('/todos')
async def get_todos():
    todos = []
    for todo in collection.find():
        todos.append(todo)
    return todos


@app.get('/todos/{todo_id}')
async def get_todo(todo_id: str):
    todo = collection.find_one({'_id': ObjectId(todo_id)})
    if todo:
        return todo
    else:
        return {'message': 'ToDo not found'}

@app.put('/todos/{todo_id}')
async def update_todo(todo_id: str, todo: ToDo):
    result = collection.update_one(
        {'_id': ObjectId(todo_id)},
        {'$set': todo.dict()},
    )
    if result.modified_count == 1:
        return {'message': 'ToDo updated successfully'}
    else:
        return {'message': 'ToDo not found'}

@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: str):
    result = collection.delete_one({'_id': ObjectId(todo_id)})
    if result.deleted_count == 1:
        return {'message': 'ToDo deleted successfully'}
    else:
        return {'message': 'ToDo not found'}
