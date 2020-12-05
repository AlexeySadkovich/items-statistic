import os

from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_INITDB_DATABASE")

MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

client = MongoClient(MONGO_HOST, int(MONGO_PORT), username=MONGO_USER, password=MONGO_PASS)
db = client[MONGO_DB]
