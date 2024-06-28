from fastapi import FastAPI, HTTPException, Depends, status
from typing import Optional
from routers import role, user, auth

app = FastAPI()

def config_router():
    app.include_router(role.router)
    # app.include_router(user.router)
    app.include_router(auth.router)
    
config_router()