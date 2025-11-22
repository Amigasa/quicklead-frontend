from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(BaseModel):
    name: str

class Project(ProjectBase):
    id: int
    api_key: str
    applications_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    client_name: str
    phone: str
    project_id: int

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    status: str = "новая"
    application_date: datetime
    created_at: datetime
    project_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User