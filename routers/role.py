from Models.role import * 
from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from database import SessionLocal
from sqlalchemy.orm import Session
import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db())]

router = APIRouter(
    prefix= '/roles',
    tags=['roles'],
    responses={404: {"description": "Not found"}},
)



def get_role_by_id(db:Session , id:int):
    return db.query(models.Role).filter(models.Role.id == id).first()

@router.get('/{name}')
def read_item(name):
    for item in Roles_db:
        if item['name'] == name:
            return item
    return {'item_name' : name}

@router.get('/')
def get_roles():
    return Roles_db

@router.post('/')
async def create_role(name: Roles):
    roles = Roles_db.routerend(name)
    
    return Roles_db[-1]

@router.delete('/{id}')
async def delete_role(name: str):
    for item in Roles_db:
        if item['id'] == id:
            Roles_db.remove(item)
            return {'item_name' : id, 'roles' : Roles_db}

    return {'not found' :  id}

@router.put('/{id}')
async def update_role(id: int, Roles: Roles):
    
    for item in Roles_db:
        if item['roleId'] == id:
            item['status'] = Roles.status
            return {'item_name' : item['name'], 'roles' : Roles_db}
        
    return {'msg' : f" roleId {id} successfully updated"}


    