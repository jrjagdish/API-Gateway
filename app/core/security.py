import secrets
import hashlib
from datetime import datetime,timedelta, timezone
import os
from typing import Optional
import bcrypt
from passlib.context import CryptContext
from jose import JWTError,jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM or 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7))

def hash_password(password:str):
    return pwd_context.hash(password[:72])

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password[:72],hashed_password)

def create_access_token(subject:str,expires_delta: Optional[timedelta] = None):
    now = datetime.utcnow()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub':str(subject),
        'iat':now,
        'exp':now+expires_delta,
        'type':'access'
    }  
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        return payload
    except JWTError as e:
        raise

#refresh token helper 
def generate_raw_refresh_token():
    return secrets.token_urlsafe(48)

def hash_refresh_token(raw:str):
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def create_refresh_token_pair(user_id: int, expires_days: Optional[int] = None):
    raw = generate_raw_refresh_token()
    hashed = hash_refresh_token(raw)

    if expires_days is None:
        expires_days = REFRESH_TOKEN_EXPIRE_DAYS

    expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)

    return raw, hashed, expires_at
   


def generate_api_key():
    raw = secrets.token_urlsafe(32)
    hased = hash_api_key(raw)
    return raw,hased

def hash_api_key(raw_key:str):
    return bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt()).decode()

def verify_api_key(raw_key: str, stored_hash: str):
    return bcrypt.checkpw(raw_key.encode(), stored_hash.encode())
