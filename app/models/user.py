from pydantic import BaseModel, Field, EmailStr, validator
import uuid
from bson import ObjectId
import re

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    @validator('password')
    def password_match(cls, v: str):
        if len(v) < 8:
            raise ValueError('Password must at least 8 characters')
        elif not re.match(r'[A-Z]', v):
            raise ValueError('Pusworm must contain at least 1 uppercase letter')
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "Nick",
                "email": "nick@gmail.com",
                "password": "weakpassword"
            }
        }