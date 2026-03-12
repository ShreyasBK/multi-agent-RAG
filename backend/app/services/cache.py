"""Upstash Redis semantic cache for LLM responses."""
from functools import lru_cache
from backend.app.core.config import settings


@lru_cache(maxsize=1)
def get_redis():
    if not settings.upstash_redis_url:
        return None
    try:
        from upstash_redis import Redis
        return Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)
    except ImportError:
        return None


def cache_get(key: str) -> str | None:
    redis = get_redis()
    if redis is None:
        return None
    return redis.get(key)


def cache_set(key: str, value: str, ttl: int = 3600) -> None:
    redis = get_redis()
    if redis is None:
        return
    redis.set(key, value, ex=ttl)
