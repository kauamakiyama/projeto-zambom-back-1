from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "atividades_db")

client: AsyncIOMotorClient = None
db: Database = None


def get_database():
    return db


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    print("✅ Conectado ao MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ Conexão MongoDB fechada")
