from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional
from app.db.models import User,Refresh_token
from app.db.session import SessionLocal
from app.schemas.user import RegisterPayload,LoginPayload,TokenResponse,UserResponse
from app.core import security

outh2_scheme = HTTPBearer()
router = APIRouter(prefix='/auth',tags=['auth'])

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(payload:RegisterPayload,db:Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email alredy registered")

    hashed = security.hash_password(payload.password)
    user =  User(email = payload.email,password_hash=hashed,name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login',response_model = TokenResponse)
def login(payload:LoginPayload,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not security.verify_password(payload.password ,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid credentials')

    access_token = security.create_access_token(subject=str(user.id))
    raw_refresh,hashed_refresh,expires_at = security.create_refresh_token_pair(user.id)

    rt_save = Refresh_token(
        user_id = user.id,
        refresh_token = hashed_refresh,
        user_agent=None,
        ip_address=None,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        is_revoked=False
    )
    db.add(rt_save)
    db.commit()
    db.refresh(rt_save)
    return TokenResponse(access_token=access_token,refresh_token=raw_refresh)

@router.post('/refresh', response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    hashed = security.hash_refresh_token(refresh_token)

    rt = db.query(Refresh_token).filter(
        Refresh_token.refresh_token == hashed,
        Refresh_token.is_revoked == False
    ).first()

    if not rt:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

   
    if rt.expires_at and rt.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    
    access_token = security.create_access_token(subject=str(rt.user_id))

   
    raw_new, hashed_new, expires_at = security.create_refresh_token_pair(rt.user_id)
    rt.refresh_token = hashed_new
    rt.expires_at = expires_at

    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=raw_new)


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    hashed = security.hash_refresh_token(refresh_token)
    rt = db.query(Refresh_token).filter(Refresh_token.refresh_token == hashed, Refresh_token.is_revoked == False).first()
    if not rt:
       
        return {"ok": True, "detail": "Token not found or already revoked"}

    rt.is_revoked = True
    db.commit()
    return {"ok": True}

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(outh2_scheme),
    db: Session = Depends(get_db)
):
    try:
        raw_token = token.credentials  
        payload = security.decode_access_token(raw_token)
        
        # Check if payload contains an error (from Option 1)
        if isinstance(payload, dict) and "error" in payload:
            raise HTTPException(status_code=401, detail=payload["detail"])
            
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
        
    except JWTError as e:  # ✅ Specifically catch JWT errors
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
