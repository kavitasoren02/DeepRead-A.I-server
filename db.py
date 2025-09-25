from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb+srv://deepreaduser:6AYzrTKbeVYOfcNI@cluster0.a2qoi9r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["deepreadAI"]

users_collection = db["users"]
file_collection = db["file_uploads"]
records_collection = db["records"]

users_collection.create_index("email", unique=True)
