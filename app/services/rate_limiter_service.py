from app.services.redis_service import redis_client

RATE_LIMIT =30
WINDOW = 60

def is_rate_limited(api_key:str):
    key = f"rate-limit:{api_key}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)
    return count > RATE_LIMIT