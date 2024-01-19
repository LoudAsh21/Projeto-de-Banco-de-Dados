from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt


def conect() -> object:
    try:
        uri = "mongodb+srv://thiago:123@cluster0.96bnu2r.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client
    except:
        return False


def insert(collection_name: str,  database: object, data: dict) -> bool:
    try:
        collection = database[collection_name]
        collection.insert_one(data)
        return True
    except:
        return False


def select(collection_name: str, database: object, filter: dict = {}) -> dict:
    try:
        collection = database[collection_name]
        data = collection.find(filter)
        return data
    except:
        return False


def update(collection_name: str, database: object, filter: dict, new_value: dict) -> bool:
    try:
        collection = database[collection_name]
        collection.update_one(filter, new_value)
        return True
    except:
        return False


def delete(collection_name: str, database: object, filter: dict) -> bool:
    try:
        collection = database[collection_name]
        collection.delete_one(filter)
        return True
    except:
        return False



