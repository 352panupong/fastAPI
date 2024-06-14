from typing import  Union
import models
from database import engine, SessionLocal
from pydantic import BaseModel

models.Base.metadata.create_all(bind = engine)

class UserBase(BaseModel):
    username : str
    password : str
    email : str
    first_name : str
    last_name : str
    phone : str
    address : str
    city : str
    
class RoleBase(BaseModel):
    role_name : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
   username: Union[str, None] = None