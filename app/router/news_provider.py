from fastapi import APIRouter, Depends, HTTPException, Query
import httpx
from app.router.auth import get_db
from app.utils.rate_limiter import track_usage
from app.utils.require_api_key import require_api_key
from app.core.config import settings
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/")
async def get_news(
    topic: str = Query(..., description="News topic to search"),
    api_key_record = Depends(require_api_key),
    db:Session = Depends(get_db)
):

    url = f"https://newsdata.io/api/1/news"
    params = {
        "apikey": settings.NEWS_API_KEY,
        "q": topic
    }
    project_id = api_key_record.project_id 
    await track_usage("news", db, project_id) 

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(500, "News provider error")

    data = response.json()

    return {
        "project_id": api_key_record.project_id,
        "service": "news",
        "data": data
    }
