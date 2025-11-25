from fastapi import APIRouter, Depends, HTTPException
from app.services.weather_service import fetch_weather
from app.utils.rate_limiter import track_usage
from app.utils.require_api_key import require_api_key
from sqlalchemy.orm import Session
from app.router.auth import get_db

router = APIRouter(prefix="/api/weather", tags=["weather"])

@router.get("/")
async def get_weather(city: str, api_key_record = Depends(require_api_key),db:Session = Depends(get_db)):
    
    project_id = api_key_record.project_id
    await track_usage("weather", db, project_id)
    data = await fetch_weather(city)

    if not data:
        raise HTTPException(status_code=404, detail="City not found or API error")

    return {
        "project_id": project_id, "service": "weather", "data": data
    }

