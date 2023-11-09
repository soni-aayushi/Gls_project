from pydantic import BaseModel
from datetime import datetime



class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    message: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    session_token:str
    status:bool
    created_date:datetime


class ResetPassword(BaseModel):
    token: str
    new_password: str
