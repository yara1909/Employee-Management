from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class ActivityLogItem(BaseModel):
    action: str
    timestamp: datetime


class User(BaseModel):
    username: str
    email: EmailStr
    role: str 

class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(User):
    userid: str
    activity_log: List[ActivityLogItem] = Field(default_factory=list)
