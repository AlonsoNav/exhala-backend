from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    logger.error("MONGO_URI is not set in the .env file")
    raise ValueError("MONGO_URI is not set in the .env file")

try:
    conn = MongoClient(mongo_uri)
    db = conn.exhalabackend  # Database name
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise
