from fastapi import HTTPException, Request
from backend.app.services.cache import get_redis
from backend.app.core.config import settings


async def rate_limit(request: Request, user_id: str) -> None:
    redis = get_redis()
    if redis is None:
        return  # skip if Redis not configured

    key = f"rate_limit:{user_id}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)  # 1-minute window

    if count > settings.api_rate_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.api_rate_limit} requests/minute",
        )
