from fastapi import APIRouter, Depends, HTTPException
from app.services.currency_sevice import convert_currency
from app.utils.rate_limiter import track_usage
from app.utils.require_api_key import require_api_key
from app.router.auth import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/currency", tags=["currency"])

@router.get("/")
async def get_currency(
    from_currency: str,
    to_currency: str,
    amount: float = 1,
    api_key_record = Depends(require_api_key),
    db: Session =  Depends(get_db)
):

    project_id = api_key_record.project_id
    await track_usage("news", db, project_id)
    result = await convert_currency(from_currency, to_currency, amount)

    if not result:
        raise HTTPException(status_code=400, detail="Invalid currency or API error")

    return {
        "project_id": project_id, "service": "currency", "data": result
    }
