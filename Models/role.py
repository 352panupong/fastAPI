from pydantic import BaseModel
from typing import Optional

class Roles(BaseModel):
    roleId : str
    name : str
    status : bool
    created_at : str
    # description : Optional[str] = None
    
    
Roles_db = [
    {
        'roleId': 1,
        "name" : "admin",
        "status" : True,
        "created_at" : "2021-04-01"
    },
    {
        'roleId': 2,
        "name" : "user",
        "status" : True,
        "created_at" : "2021-04-01"
    }
]