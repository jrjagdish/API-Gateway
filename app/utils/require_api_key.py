from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.models import Api_Keys
from app.router.auth import get_db
import bcrypt


async def require_api_key(
    x_api_key: str = Query(..., alias="api_key"),
    db: Session = Depends(get_db)
):
    key_records = db.query(Api_Keys).filter(Api_Keys.is_active == True).all()

    if not key_records:
        raise HTTPException(status_code=401, detail="Invalid API key")

    matched = None
    for key in key_records:
        try:
            # Ensure the stored hash is a valid bcrypt hash
            if bcrypt.checkpw(x_api_key.encode(), key.key_hash.encode()):
                matched = key
                break
        except ValueError:
            # Handle invalid hash format - might be from old hashing method
            continue

    if not matched:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return matched