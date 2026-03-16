import redis.asyncio as redis
import json
import os
from typing import Optional, Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)

async def get_cached(key: str) -> Optional[Any]:
    r = await get_redis()
    value = await r.get(key)
    if value:
        print(f"Cache HIT: {key}")
        return json.loads(value)
    print(f"Cache MISS: {key}")
    return None

async def set_cached(key: str, value: Any, ttl_seconds: int = 300):
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=ttl_seconds)