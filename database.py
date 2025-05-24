from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_DETAILS = config("MONGO_URL")  

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.todo_db
task_collection = database.get_collection("tasks")
