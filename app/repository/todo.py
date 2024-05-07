from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId

from app.schemas.todo import ToDo
from app.data_adapter.db import collection


class ToDoRepository:
    def __init__(self, collection):
        self.collection = collection

    async def __call__(self, method, *args, **kwargs):
        if method == 'create_todo':
            return await self.create_todo(*args, **kwargs)
        elif method == 'get_all_todos':
            return await self.get_all_todos(*args, **kwargs)
        elif method == 'get_todo_by_id':
            return await self.get_todo_by_id(*args, **kwargs)
        elif method == 'update_todo':
            return await self.update_todo(*args, **kwargs)
        elif method == 'delete_todo':
            return await self.delete_todo(*args, **kwargs)

    async def create_todo(self, todo: ToDo) -> ToDo:
        todo_data = todo.dict()
        result = self.collection.insert_one(todo_data)
        inserted_todo = await self.collection.find_one({'_id': result.inserted_id})
        return ToDo(**inserted_todo)

    async def get_all_todos(self) -> list[ToDo]:
        todos = []
        for todo in self.collection.find():
            todos.append(ToDo(**todo))
        return todos

    async def get_todo_by_id(self, todo_id: str) -> ToDo:
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        todo = await self.collection.find_one({'_id': ObjectId(todo_id)})
        if not todo:
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        return ToDo(**todo)

    async def update_todo(self, todo_id: str, todo: ToDo) -> ToDo:
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')

        existing_todo = await self.collection.find_one({'_id': ObjectId(todo_id)})
        if not existing_todo:
            raise HTTPException(status_code=404, detail='ToDo Not found')

        update_result = await self.collection.update_one(
            {'_id': ObjectId(todo_id)},
            {'$set': todo.dict()}
        )
        if udate_result.modified_count != 1:
            raise HTTPException(status_code=500, detail='Failed to update ToDo')

        updated_todo = await self.collection.find_one({'_id': ObjectId(todo_id)})
        return ToDo(**updated_todo)

    async def delete_todo(self, todo_id: str) -> None:
        if not ObjectId.isvalid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        delete_result = await self.collection.delete_one(
            {'_id': ObjectId(todo_id)}
        )
        if delete_result.deleted_count != 1:
            raise HTTPException(status_code=404, detail='ToDo Not found')

