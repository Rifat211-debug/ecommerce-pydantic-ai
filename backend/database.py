import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path = os.path.join(os.getcwd(), ".env"))

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# Initialize MongoDB database

db = client["ecommerce_db"]

# collections

users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]
cart_collection = db["cart"]
