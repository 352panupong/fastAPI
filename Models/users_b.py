from sqlalchemy import Column, Integer, String, create_engine,DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Database_URL = 'mysql://root:root@localhost:3306/bluehouse'

Base = declarative_base()

class Roles(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String)
    
    users = relationship('User', back_populates="role")
    
class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    username = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    first_name = Column(String, index=True, )
    last_name = Column(String, index=True, )
    phone = Column(String, index=True)
    address = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    role_id = Column(Integer,ForeignKey('roles_role_id'), nullable= False, )
    
    
    role = relationship("Role", back_populates="users")
    
engine = create_engine(Database_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)