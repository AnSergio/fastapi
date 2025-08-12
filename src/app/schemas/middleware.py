
from fastapi import Request
from fastapi_limiter.depends import RateLimiter
from starlette.middleware.base import BaseHTTPMiddleware


class DocsRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in ["/docs", "/redoc"]:  # ou qualquer outro endpoint que queira limitar
            # Aplica a limitação: 6 requisições por minuto
            limit = RateLimiter(times=6, seconds=60)
            return await limit(request, call_next)
        return await call_next(request)
