from sqlalchemy import Boolean,  Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, nullable = False, index=True, autoincrement=True)
    username = Column(String(45), index=True, unique = True)
    password = Column(String(200),)
    email = Column(String(45) )
    first_name = Column(String(45))
    last_name = Column(String(45))
    phone = Column(String(10))
    address = Column(String(200))
    city = Column(String(45))
    created_at = Column(DateTime)    

class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, nullable = False, index=True, autoincrement=True)
    role_name = Column(String(45))
    created_at = Column(DateTime)
    status = Column(Boolean)
    
    
class User_has_role(Base):
    __tablename__ = "user_has_role"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, primary_key=True, nullable=False)
    