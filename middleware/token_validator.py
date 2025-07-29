# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from tools.smart_marker_injector import auto_function
from tools.obvious_router import auto_function
# @auto_function
from handler import auto_logic
from handler import auto_route
from handler import auto_model
# ╔════════════════════════════════════════════════════╗
# ║         TOKEN VALIDATOR MIDDLEWARE & DECORATORS   ║
# ╚════════════════════════════════════════════════════╝

from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

# 🧠 Dummy in-memory token mapping (later connect to DB)
FAKE_TOKENS = {
    "admin-token-123": "admin",
    "dev-token-456": "developer",
    "user-token-789": "user"
}

# 🧱 Global Middleware
class TokenValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token or token not in FAKE_TOKENS:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        request.state.role = FAKE_TOKENS[token]
        response = await call_next(request)
        return response


# 🔐 Decorators
@auto_model
@auto_route
@auto_logic
def admin_only(route_func):
    async def wrapper(request: Request, *args, **kwargs):
        if request.state.role != "admin":
            raise HTTPException(status_code=403, detail="Admins only")
        return await route_func(request, *args, **kwargs)
    return wrapper


@auto_model
@auto_route
@auto_logic
def developer_only(route_func):
    async def wrapper(request: Request, *args, **kwargs):
        if request.state.role != "developer":
            raise HTTPException(status_code=403, detail="Developers only")
        return await route_func(request, *args, **kwargs)
    return wrapper

