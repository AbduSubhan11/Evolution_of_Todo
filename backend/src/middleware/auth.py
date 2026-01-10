from fastapi import HTTPException, status, Request
from ..auth.security import verify_token, verify_better_auth_token, get_current_user_id
from typing import Optional
import uuid

async def jwt_auth_middleware(request: Request, call_next):
    """
    Middleware to validate JWT tokens in requests
    This will check for Authorization header and validate the JWT token
    Supports both custom backend tokens and Better Auth tokens
    """
    # Skip auth for OPTIONS requests (preflight CORS requests)
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    # Skip auth for public endpoints
    if request.url.path in ["/", "/health", "/docs", "/redoc", "/openapi.json", "/api/auth/register", "/api/auth/login", "/api/auth/logout", "/api/auth/health"]:
        response = await call_next(request)
        return response

    # Check for Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid"
        )

    token = auth_header.split(" ")[1]
    try:
        user_id = get_current_user_id(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Add user_id to request state for use in endpoints
    request.state.user_id = user_id

    response = await call_next(request)
    return response