from app.core.security import generate_api_key, hash_api_key
from app.db.session import SessionLocal
from app.db.models import Api_Keys
from datetime import datetime, timedelta

DEFAULT_EXPIRE_DAYS = 30

def create_api_key_for_project(owner: str, owner_type: str, project_id: int = None, expires_days: int = DEFAULT_EXPIRE_DAYS):

    raw,hashed_key = generate_api_key()
    db = SessionLocal()
    try:
        api = Api_Keys(
            key_hash=hashed_key,
            owner=owner,
            owner_type=owner_type,
            project_id=project_id,
            created_at=datetime.utcnow(),
            expires_at=(datetime.utcnow() + timedelta(days=expires_days))
        )
        db.add(api)
        db.commit()
        db.refresh(api)
        return {"raw_key": raw, "api_key_id": api.id}
    finally:
        db.close()

def revoke_api(api_key_id:int):
    db = SessionLocal()
    try:
        api = db.query(Api_Keys).get(api_key_id)
        if not api:
            return False
        api.is_active = False
        db.commit()
        return True
    finally:
        db.close()        
