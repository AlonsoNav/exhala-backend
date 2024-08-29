from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

conn = MongoClient(mongo_uri)
db = conn.exhalabackend  # Name of the database
