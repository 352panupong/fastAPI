from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Header
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
import Schemas as schemas
import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix= '/users',
    tags=['users'],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
async def getUser(db:db_dependency):
    return db.query(models.User).all()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserBase, db:db_dependency): 
    db_user = db.query(models.User).filter(models.User.username==user.username).first()
    new_user = models.User(**user.model_dump)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



