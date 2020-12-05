from pymongo import MongoClient
from core.config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASS


client = MongoClient(MONGO_HOST, int(MONGO_PORT), username=MONGO_USER, password=MONGO_PASS)
db = client[MONGO_DB]
