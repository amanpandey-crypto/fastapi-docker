from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmployeeSchema(BaseModel):
    emp_id: str = Field(...)
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    department: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "emp_id": 1,
                "fullname": "Full_name",
                "email": "something@x.com",
                "department": "department"
            }
        }


class UpdateEmployeeModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Full_name",
                "email": "something@x.com",
                "department": "department"
            }
        }


    
class UserSchema(BaseModel):
    fullname: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Full_name",
                "username": "user_name",
                "password": "********"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "user_name",
                "password": "*********"
            }
        }