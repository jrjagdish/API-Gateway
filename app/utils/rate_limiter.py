from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import ApiUsage
from app.router.auth import get_db

DAILY_LIMIT = 5

async def track_usage(service: str, db: Session, project_id: int):
    today = datetime.utcnow().date()

    count = (
        db.query(ApiUsage)
        .filter(
            ApiUsage.project_id == project_id,
            ApiUsage.service == service,
            ApiUsage.timestamp >= today
        )
        .count()
    )

    if count >= DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit of {DAILY_LIMIT} requests for {service} exceeded"
        )

    usage = ApiUsage(project_id=project_id, service=service)
    db.add(usage)
    db.commit()
