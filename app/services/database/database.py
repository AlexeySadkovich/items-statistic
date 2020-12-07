import motor.motor_asyncio
from core.config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASS


MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]
