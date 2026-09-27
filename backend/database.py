from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
client = None
database = None

async def connect_to_database():
    global client, database
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        # Test connection
        await client.admin.command('ping')
        database = client.gwadar_cargo_network
        print("Connected to MongoDB successfully")
        return database
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def close_database_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_database():
    return database
