from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import json
import base64


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create a JWT refresh token with longer expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # 7 days for refresh token
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None

def verify_better_auth_token(token: str) -> Optional[dict]:
    """
    Verify a Better Auth JWT token.
    For this to work, Better Auth should be configured with the same secret as the backend.
    """
    try:
        # Better Auth tokens use the same underlying JWT technology
        # If Better Auth is configured with the same secret, this should work
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        # If the token doesn't match our secret, it might be a Better Auth token with its own secret
        # In a real implementation, you'd need to share secrets or use a different approach
        try:
            # Attempt to decode without verification to inspect the token structure
            # This is safe as we're not trusting the contents, just inspecting structure
            unverified_payload = jwt.get_unverified_claims(token)

            # Check if this looks like a Better Auth token by examining claims
            if 'sid' in unverified_payload or 'role' in unverified_payload:
                # This appears to be a Better Auth token
                # For this to work properly, you'd need to configure Better Auth to use the same secret
                # or implement proper public key verification
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                    return None
                return payload
        except JWTError:
            pass

        return None

def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify a refresh token and return the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "refresh":
            return None
        return payload
    except JWTError:
        return None

def get_current_user_id(token: str) -> Optional[uuid.UUID]:
    """Extract user ID from a JWT token."""
    # Try both regular and Better Auth token verification
    payload = verify_token(token) or verify_better_auth_token(token)
    if payload is None:
        return None
    user_id = payload.get("sub")
    try:
        return uuid.UUID(user_id)
    except ValueError:
        return None