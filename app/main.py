import asyncio
import time
from fastapi import FastAPI, Request
from sqlalchemy import text
from app.db.init_db import init_db
from app.db.models import RequestLog
from app.db.session import SessionLocal
from app.router import auth
from app.services.provider_service import rate_limit_middleware



app = FastAPI()

app.middleware('http')(rate_limit_middleware)

async def delete_old_logs():
    while True:
        await asyncio.sleep(60 * 60 * 12)  # every 12 hours

        db = SessionLocal()
        db.execute(text("""
            DELETE FROM request_logs
            WHERE created_at < NOW() - INTERVAL '24 HOURS';
        """))
        db.commit()
        db.close()

@app.on_event('startup')
def startup():
    init_db()

def save_log(method, path, status_code, ip, duration):
    db = SessionLocal()
    log = RequestLog(
        method=method,
        path=path,
        status_code=status_code,
        response_time_ms=duration,
        ip=ip
    )
    db.add(log)
    db.commit()
    db.close()  

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    ip = request.client.host

    # Save log asynchronously (non-blocking)
    save_log(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        ip=ip,
        duration=duration
    )

    return response

@app.get('/')
def root():
    return {"message" : "API gateway is running!"}   

app.include_router(auth.router) 