# app/schemas/auth.py
from pydantic import BaseModel, EmailStr

class RegisterPayload(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None  

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str | None

    class Config:
        from_attributes = True
