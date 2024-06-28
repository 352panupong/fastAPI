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
    prefix= '/projects',
    tags=['projects'],
    responses={404: {"description": "Not found"}},)


@router.get('/')
def get_project(project= schemas.user_has_project, db=db_dependency):
    return db.query(models.Project).all()

async def add_project(project: schemas.user_has_project, db=SessionLocal):
    models.Project(**project.model_dump)
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project

@router.get('/{id}/{user_id}')
def get_project_by_id(id: int, user_id : int ,project= schemas.user_has_project, db=db_dependency):
    return db.query(models.Project).filter(models.Project.id == id, models.Project.user_id).first()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def created_project(project:schemas.user_has_project, db=db_dependency):
    try:
        new_project = await add_project(project, db)
        output = {'status' : 'success', 'data' : project.project_name}
    except Exception as e: 
        print(f"Error: {str(e)}")
        output = {'status' : 'error', 'data' : str(e)}
    return output

@router.delete('/{id}/{user_id}')
def delete_project(id: int, user_id : int, project= schemas.user_has_project, db=db_dependency):
    try : 
        project = db.query(models.Project).filter(models.Project.id == id, models.Project.user_id == user_id).first()
        db.delete(project)
        db.commit()
        output = {'status' :'success', 'data' : project.project_name}
    except Exception as e:
        output = {'status' :'error', 'message' : str(e.message)}
    return output

@router.put('/{id}/{user_id}', status_code=status.HTTP_200_OK)
def update_project(id: int, user_id : int, project= schemas.user_has_project, db=db_dependency):
    try : 
        project = db.query(models.Project).filter(models.Project.id == id, models.Project.user_id == user_id).first()
        project.project_name = project.project_name
        db.commit()
        output = {'status' :'success', 'data' : project.project_name}
    except Exception as e:
        output = {'status' :'error', 'message' : str(e.message)}
    return output
