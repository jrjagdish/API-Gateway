from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.router.auth import get_db
from app.db.models import Project
from app.schemas.project import ProjectCreate
from app.services.api_key_service import create_key
from app.router.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", status_code=201)
def create_project(payload: ProjectCreate,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):

   
    project = Project(
        name=payload.name.strip(),
        description=payload.description.strip() if payload.description else None,
        owner_user_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(project)
    db.commit()  
    db.refresh(project)    
    

   
    return {
        "project_id": project.id,
        "name": project.name,
        "owner_id":project.owner_user_id,
        "description": project.description,
        "created_at": project.created_at,
       
    }
