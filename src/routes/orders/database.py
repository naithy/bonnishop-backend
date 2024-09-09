from pymongo import MongoClient

from src.config import MONGODB_CONNECT

client = MongoClient(MONGODB_CONNECT)

db = client['users']

collection_name = db['orders']
