from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email:EmailStr
    password : str
    name: str|None = None

class UserResponse(BaseModel):
    id:int 
    email:EmailStr
    name:str | None

    class config:
        from_attributes = True   