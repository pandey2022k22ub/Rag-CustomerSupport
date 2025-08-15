from pymongo import MongoClient
import os

# MongoDB connection details (use env vars or defaults)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "nerve_spark")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
knowledge_base_collection = db["knowledge_base"]
