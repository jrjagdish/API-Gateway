from fastapi import Request, HTTPException
from app.services.rate_limiter_service import is_rate_limited

async def rate_limit_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-KEY")

    if api_key:
        if is_rate_limited(api_key):
            raise HTTPException(status_code=429, detail="Rate limit exceeded (30 req/min)")

    return await call_next(request)