from app.core.security import generate_api_key, hash_api_key
from sqlalchemy.orm import Session
from app.db.models import Api_Keys
from datetime import datetime, timedelta

DEFAULT_EXPIRE_DAYS = 30

def create_key(db: Session, project_id: int):

    raw, hashed = generate_api_key()

    api = Api_Keys(
        key_hash=hashed,
        owner=str(project_id),
        owner_type="project",
        project_id=project_id,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=30),
        last_used_at = datetime.utcnow()
    )

    db.add(api)
    db.commit()
    db.refresh(api)

    return {"raw_key": raw, "api_key_id": api.id}
       
