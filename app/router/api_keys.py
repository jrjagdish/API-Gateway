from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.models import Project
from app.router.auth import get_db,get_current_user
from app.services.api_key_service import create_key

router = APIRouter()

@router.post("/projects/{project_id}/apikey")
def create_api_key(project_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    project = db.query(Project).filter(Project.id == project_id, Project.owner_user_id == current_user.id).first()
    

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = create_key(db=db, project_id=project.id)
    base_url = "https://api-gateway-dxr3.onrender.com/"  # In production, use your domain
    
    # Usage examples with the new API key
    usage_examples = {
        "weather": f"{base_url}/api/weather?city=London&api_key={result['raw_key']}",
        "currency": f"{base_url}/api/currency?from_currency=USD&to_currency=EUR&amount=10&api_key={result['raw_key']}",
        "news": f"{base_url}/api/news?topic=technology&api_key={result['raw_key']}"
    }

    return {"api_key": result["raw_key"],"usage_example":usage_examples}
