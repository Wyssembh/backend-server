
from pydantic import BaseModel
from datetime import datetime



class User(BaseModel):
    username:str
    lastname:str
    poste:str
    telephone:int
    cin:int
    address:str
    departement:str
    




class VacationRequest(BaseModel):
    user_cin :int
    username:str 
    lastname: str
    start_date: str
    end_date: str
    type: str
    submitted_at: datetime = datetime.now() 
    status: str = "pending"

class UpdateVacationStatusRequest(BaseModel):
    status: str  
class Post(BaseModel):
    title: str
    content: str
    address: str




    



