"""
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://local postgres:wissem0430a@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""

import os
import gridfs
from motor.motor_asyncio import AsyncIOMotorClient
# MongoDB connection URL (update with your credentials)
MONGO_URL = "mongodb://localhost:27017"

# Create a MongoDB client
client = AsyncIOMotorClient(MONGO_URL)

# Select the database
db = client["project"]  # Replace with your actual database name
users_collection = db["users"]
vacations_collection = db["vacations"]
posts_collection=db["posts"]
pdf_collection = db["pdfs"]
login_collection=db["login"]
#fs = gridfs.GridFS(db)

def get_db():
    return db