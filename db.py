from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017")

db = client["deepreadAI"]

users_collection = db["users"]
file_collection = db["file_uploads"]
records_collection = db["records"]

users_collection.create_index("email", unique=True)
