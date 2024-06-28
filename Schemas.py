from typing import  Union
import models
from database import engine, SessionLocal
from pydantic import BaseModel
from datetime import datetime

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
    # role_id : int
    role_name : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
   username: Union[str, None] = None
   
class user_has_role(UserBase):
    user_id : int
    role_id : int
    
class user_has_project(UserBase):
    user_id :  int
    project_name : str
    description : str