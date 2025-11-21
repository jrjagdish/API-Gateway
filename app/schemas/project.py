from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
