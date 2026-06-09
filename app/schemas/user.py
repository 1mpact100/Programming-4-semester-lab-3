import re

from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.currency import CurrencyRead

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class UserCreate(BaseModel):
    username: str
    email: str
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        
        if not value:
            raise ValueError("Username cannot be empty")
        
        return value
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip()
        
        if not EMAIL_RE.match(value):
            raise ValueError("Invalid email format")
        
        return value

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str | None) -> str | None:
        if value is None:
            return value
        
        value = value.strip()
        
        if not value:
            raise ValueError("Username cannot be empty")
        
        return value
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        
        value = value.strip()
        
        if not EMAIL_RE.match(value):
            raise ValueError("Invalid email format")
        
        return value

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str

class UserWithSubscriptions(UserRead):
    subscriptions: list[CurrencyRead]
