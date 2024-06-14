from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal, engine
from typing import Annotated, Optional
import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import Schemas as schemas
import models
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "ly$Ce54oOSAbIfQ73gl#6PPGB@BP34SnTnppqq3#NcjZpu#CPfINsjF4J%mPj1mc"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
   
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix= '/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}},
)

async def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

async def get_user_by_username(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()


async def create_user(db:Session, user : schemas.UserBase):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username = user.username,
        password =  hashed_password,
        email = user.email,
        first_name = user.first_name,
        last_name = user.last_name,
        phone = user.phone,
        address = user.address,
        city = user.city,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db:Session, username:str, password:str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def verify_password(password, heshed_password:str):
    return pwd_context.verify_password(password, heshed_password)

def create_access_token(data : dict, expires_delta : Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password):
    return pwd_context.hash(password)


#  URL parameters for authentication

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserBase, db:db_dependency): 
    db_user = get_user_by_email(user.email)
    if db_user : 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db=db, user = user)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {'sub' : user.username} , expires_delta=access_token_expires
        )
    
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
    