import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter


async def redis_url(url: str):
    redis_url = await redis.from_url(url, encoding="utf-8", decode_responses=True)
    return await FastAPILimiter.init(redis_url)
