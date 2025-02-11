import jwt
import datetime
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from database import users_collection

load_dotenv()

SECRET_KEY = os.getenv("e6a1c3b8c9b74f4aa8d3e1c0a5f7e2d7f2c4b0d8a9e3f6c5b7a1c2d3e4f5a6b", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake users database (exemple)
users_db = {
    "project": {"username": "admin", "password": pwd_context.hash("admin123"), "role": "admin"}
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return user
"""
async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})  # Recherche l'utilisateur dans MongoDB
    if not user or user["password"] != password:  # Comparaison basique, remplace par Hash de mot de passe
        return None
    return user
"""
def create_access_token(username: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": username, "exp": expire}
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Security(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in users_db:
            raise HTTPException(status_code=401, detail="Utilisateur non autorisé")
        return users_db[username]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
