from fastapi import FastAPI, HTTPException
from bson.objectid import ObjectId

from app.schemas.todo import ToDo
from app.data_adapter.db import collection


class ToDoRepository:
    def __init__(self, collection):
        self.collection = collection

    def create_todo(self, todo: ToDo) -> ToDo:
        """
        Create a new ToDo item.
        """
        todo_data = todo.dict()
        result = self.collection.insert_one(todo_data)
        inserted_todo = self.collection.find_one({'_id': result.inserted_id})
        return {
            '_id': str(inserted_todo['_id']),
            'title': todo.title,
            'description': todo.description
        }

    def get_all_todos(self) -> list[ToDo]:
        """
        Get all ToDo items.
        """
        todos = []
        for todo in self.collection.find():
            todos.append({
                '_id': str(todo['_id']),
                'title': todo['title'],
                'description': todo['description']
            })
        return todos

    def get_todo_by_id(self, todo_id: str) -> ToDo:
        """
        Get a specific ToDo item by ID.
        """
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        todo = self.collection.find_one({'_id': ObjectId(todo_id)})
        if not todo:
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        return ToDo(**todo)

    def update_todo(self, todo_id: str, todo: ToDo) -> ToDo:
        """
        Update a ToDo item by ID.
        """
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')

        existing_todo = self.collection.find_one({'_id': ObjectId(todo_id)})
        if not existing_todo:
            raise HTTPException(status_code=404, detail='ToDo Not found')

        update_result = self.collection.update_one(
            {'_id': ObjectId(todo_id)},
            {'$set': todo.dict()}
        )
        if update_result.modified_count == 1:
            raise HTTPException(status_code=200, detail='ToDo update successfully')

        updated_todo = self.collection.find_one({'_id': ObjectId(todo_id)})
        return ToDo(**updated_todo)

    def delete_todo(self, todo_id: str) -> None:
        """
        Delete a ToDo item by ID.
        """
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail='Invalid todo_id')
        delete_result = self.collection.delete_one(
            {'_id': ObjectId(todo_id)}
        )
        if delete_result.deleted_count != 1:
            raise HTTPException(status_code=404, detail='ToDo Not found')

