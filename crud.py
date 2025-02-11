"""
from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=user.id,username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, cin: int):
    return db.query(models.User).filter(models.User.cin == cin).first()


def get_users(db: Session):
    return db.query(models.User).all()

def submit_vacation(db: Session, vacation: schemas.VacationRequest, user_id: int):
    db_vacation = models.Vacation(**vacation.dict(), user_id=user_id)
    db.add(db_vacation)
    db.commit()
    db.refresh(db_vacation)
    return db_vacation

"""


from bson import ObjectId
from database import users_collection, vacations_collection,posts_collection
from schemas import User, VacationRequest, Post
from datetime import datetime, timedelta
from fastapi import HTTPException, status


# Convert MongoDB document to dictionary
def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

# Create User
async def create_user(user: User):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict

# Get User by CIN
async def get_user(cin: int):
    user = await users_collection.find_one({"cin": cin})
    return serialize_doc(user)

# Get All Users
async def get_users():
    users = await users_collection.find().to_list(100)  # Limit to 100 users
    return [serialize_doc(user) for user in users]

# Submit Vacation Request
async def submit_vacation(vacation: VacationRequest):
    vacation_dict = vacation.dict()
    vacation_dict["submitted_at"] = datetime.now()  # Ajout de la date de soumission
    result = await vacations_collection.insert_one(vacation_dict)
    vacation_dict["_id"] = str(result.inserted_id)
    return vacation_dict

async def get_vacations_by_user(user_cin: int):
    cursor = vacations_collection.find({"user_cin": user_cin})
    vacations = await cursor.to_list(length=None)  
    return [serialize_doc(vacation) for vacation in vacations]


async def getvacations():
    vacations = await vacations_collection.find().to_list(100)
    return [serialize_doc(vacation) for vacation in vacations]

async def get_cin(username:str):
    user = await users_collection.find_one({"username":username})
    return user["cin"]

async def create_post(post:Post):
    post_dict = post.dict()
    result = await posts_collection.insert_one(post_dict)
    post_dict["_id"] = str(result.inserted_id)
    return post_dict


async def get_posts():
    posts = await posts_collection.find().to_list(100)
    return [serialize_doc(post) for post in posts]
