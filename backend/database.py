import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path = os.path.join(os.getcwd(), ".env"))

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

# Initialize MongoDB database

db = client["ecommerce_db"]

# collections

users_collections = db["users"]
products_collections = db["products"]
orders_collections = db["orders"]
cart_collections = db["cart"]
