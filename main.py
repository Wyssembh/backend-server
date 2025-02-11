
import datetime
import os
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from pymongo import MongoClient
from schemas import Post, UpdateVacationStatusRequest, User, VacationRequest
from crud import  create_post, create_user, get_cin, get_posts, get_user, get_users, get_vacations_by_user, submit_vacation,getvacations
from database import pdf_collection, get_db, users_collection,vacations_collection , login_collection
app = FastAPI()

@app.get("/getdb/")
async def db():
    return get_db()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymongo

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginModel(BaseModel):
    username: str
    password: str
@app.post("/login/", status_code=201)
async def login(user: User):
    print(f"Attempting login for user: {user.email}")
    users = login_collection.find_one({"username": user.email, "password": user.password})
    if not users:
        print("Login failed: Invalid credentials")
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    print("Login successful")
    return {"message": 'successful', 'user': user.email}

@app.post("/users/")
async def create_user_api(user: User):
    return await create_user(user)

@app.get("/users/{cin}")
async def get_user_api(cin: int):
    user = await get_user(cin)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/")
async def get_users_api():
    return await get_users()

@app.post("/vacation")
async def submit_vacation_api( vacation: VacationRequest):
    return await submit_vacation(vacation)


@app.get("/vacations")
async def get_vacation_api():
    return await getvacations()

@app.delete("/users/{cin}/vacation/delete")
async def delete_vacation_api(cin: int):
    vacation=vacations_collection.delete_one({"user_cin": cin})
    return {"message": "vacation deleted"}

@app.get("/users/{cin}/vacations/")
async def get_vacations(cin: int):
    return await get_vacations_by_user(cin)


@app.post("/posts/")
async def create_post_api(post: Post):
    return await create_post(post)


@app.get("/posts/")
async def get_posts_api():
    return await get_posts()

@app.put("/users/{usercin}/vacation/status")
async def update_vacation_status(usercin: int, request: UpdateVacationStatusRequest):
    status = request.status
    if status not in ["pending", "accepted"]:
        raise HTTPException(status_code=400, detail="Statut invalide. Utilisez 'pending', 'accepted', ou 'rejected'.")
    result = vacations_collection.update_one(
        {"user_cin": usercin},  
        {"$set": {"status": status}}  
    )
    return {"message": "status updated"}



@app.post("/upload/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_folder = "uploads/"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"message": "Fichier téléchargé avec succès", "file_path": file_path}
    except Exception as e:
        return {"message": f"Une erreur s'est produite: {str(e)}"}




"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pymongo import MongoClient
from database import fs
import gridfs
import shutil
import os

# Dossier temporaire pour stocker les fichiers avant de les envoyer à MongoDB
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")

    # Sauvegarde temporaire
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Stocker dans GridFS
    with open(temp_path, "rb") as f:
        file_id = fs.put(f, filename=file.filename)

    # Supprimer le fichier temporaire
    os.remove(temp_path)

    return {"message": "Fichier uploadé avec succès", "file_id": str(file_id)}


@app.get("/files/")
async def list_files():
   
    files = [{"filename": file.filename, "file_id": str(file._id)} for file in fs.find()]
    return {"files": files}


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    
    file = fs.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.read())

    return FileResponse(file_path, media_type="application/pdf", filename=file.filename)


@app.delete("/delete/{file_id}")
async def delete_file(file_id: str):
   
    try:
        fs.delete(file_id)
        return {"message": "Fichier supprimé avec succès"}
    except:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
"""


"""
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/addpdf/")
async def add_pdf(file: UploadFile = File(...), description: str = ""):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store metadata in MongoDB
    pdf_metadata = {
        "filename": file.filename,
        "description": description,
        "upload_date": datetime.utcnow().isoformat(),
        "file_path": file_path,
    }
    pdf_collection.insert_one(pdf_metadata)

    return {"message": "PDF uploaded successfully", "filename": file.filename}

@app.get("/getpdfs/")
async def get_pdfs():
    pdfs = list(pdf_collection.find({}, {"_id": 0}))  # Exclude MongoDB internal ID
    return {"pdfs": pdfs}
"""
