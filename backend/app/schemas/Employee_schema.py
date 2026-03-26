#Defines Employee schema for data validation and serialization
from pydantic import BaseModel, EmailStr, Field
import datetime

class Employee(BaseModel):
    employeeID: str 
    name: str 
    email: EmailStr
    department: str
    position: str
    status: str

class EmployeeResponse(BaseModel):
    id: str 
    createdAt: datetime.datetime

class EmployeeCreate(BaseModel):
    employeeID: str 
    name: str 
    email: EmailStr
    department: str
    position: str
    status: str
    createdAt: datetime.datetime = datetime.datetime.now()

class UpdateEmployee(BaseModel):
    employeeID: str 
    name: str 
    email: EmailStr
    department: str
    position: str
    status: str
    createdAt: datetime.datetime = datetime.datetime.now()
