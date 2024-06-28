from Models.role import * 
from fastapi import APIRouter, Depends, status
from typing import Annotated, Optional
from database import SessionLocal
import Schemas as schemas
from sqlalchemy.orm import Session
import models
from datetime import datetime, timedelta

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix= '/roles',
    tags=['roles'],
    responses={404: {"description": "Not found"}},
)



def get_role_by_id(db:Session , id:int):
    return db.query(models.Role).filter(models.Role.id == id).first()

def get_role_by_name(db:Session, name:str):
    return db.query(models.Role).filter(models.Role.name == name).first()

@router.get('/')
def get_roles(role = schemas.RoleBase, db:db_dependency=None):
    return db.query(models.Role).all()
    

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_role(role: schemas.RoleBase, db:db_dependency):
    try:
        new_role = models.Role(
            role_name=role.role_name,
            created_at=datetime.now(),
            status=True,
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        output = {'status' : 'success', 'data' : role.role_name}
    except Exception as e: 
        print(f"Error: {str(e)}")
        output = {'status' : 'error', 'data' : str(e)}
    return output

@router.delete('/{id}')
async def delete_role(name: str):
    for item in Roles_db:
        if item['id'] == id:
            Roles_db.remove(item)
            return {'item_name' : id, 'roles' : Roles_db}

    return {'not found' :  id}

@router.put('/{id}')
async def update_role(id: int, Roles: Roles):
    
    return {'msg' : f" roleId {id} successfully updated"}


    