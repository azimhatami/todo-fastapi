from pymongo import MongoClient


client = MongoClient('mongodb://todo_fastapi-mongo-1:27017')
db = client['todo_db']
collection = db['todo_collection']
