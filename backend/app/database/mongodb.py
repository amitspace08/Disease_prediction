import os
from motor.motor_asyncio import AsyncIOMotorClient

# Should use env variables in production
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "disease_prediction_db"

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()

async def connect_to_mongo():
    print(f"Connecting to MongoDB at {MONGODB_URI}...")
    db.client = AsyncIOMotorClient(MONGODB_URI)
    print("Connected to MongoDB.")

async def close_mongo_connection():
    if db.client is not None:
        print("Closing MongoDB connection...")
        db.client.close()
        print("MongoDB connection closed.")

def get_database():
    return db.client[DB_NAME]
