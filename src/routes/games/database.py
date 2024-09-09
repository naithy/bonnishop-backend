from pymongo import MongoClient

from src.config import MONGODB_CONNECT

client = MongoClient(MONGODB_CONNECT)

db = client['store']

collection_name = db['games']
