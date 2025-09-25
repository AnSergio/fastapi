# src/utils/rate_limit.py
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from src.app.core.config import rdb_url


async def init_redis():
    redis_client = await redis.from_url(rdb_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
