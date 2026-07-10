from motor.motor_asyncio import AsyncIOMotorClient
import os
from .config import load_app_env

load_app_env()

# motor is the async driver for MongoDB  "async" means FastAPI won't
# freeze while waiting for the database to respond
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "shopdemo")

client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=3000)
db = client[DATABASE_NAME]

# These are your collections  equivalent to tables in SQL
customers_collection = db["customers"]
orders_collection = db["orders"]
products_collection = db["products"]
